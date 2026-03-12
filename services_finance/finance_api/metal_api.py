import logging
import requests
import xml.etree.ElementTree as et
from datetime import datetime, timedelta
from config.settings import api_metals


class MetalDataManager:
    """
    Менеджер поставки данных по драгметаллам из ЦБ РФ.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api_url = api_metals
        self.metal_rates = {}  # Здесь храниться: {1: Золото, 2: Серебро}.

    def update_rates(self):
        try:
            # 1. Установка периода: сегодня и 10 дней назад для захвата выходных.
            end_date = datetime.now().strftime("%d/%m/%Y")
            start_date = (datetime.now() - timedelta(days=10)).strftime("%d/%m/%Y")

            # 2. Формирует параметры запроса и заголовки для обхода блокировки 403.
            params = {"date_req1": start_date, "date_req2": end_date}
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
            }

            # Печатает всё, что отправляем и получаем.
            self.logger.info(f"Запрос к ЦБ: {self.api_url} с параметрами {params}")

            # 3. Выполнение запроса к API ЦБ.
            response = requests.get(self.api_url, params=params, headers=headers, timeout=10)

            self.logger.info(f"Статус ответа: {response.status_code}")

            if response.status_code == 200:  # 4. Проверка 200.
                self.logger.info(f"Сырой ответ от ЦБ: {response.text}")
                if not response.content:
                    self.logger.error("❌ ЦБ прислал пустой ответ (body is empty)")
                    return False

                # Печатает кусочек XML для проверки.
                self.logger.debug(f"XML фрагмент: {response.text[:100]}")

                # 4.1 Парсит XML. Превращает XML-текст в дерево объектов.
                root = et.fromstring(response.content)
                temp_rates = {}
                records = root.findall('Record')

                if not records:
                    self.logger.warning("⚠️ В XML нет тегов <Record>. Возможно, праздники или нет торгов.")
                    return False

                # 4.2 Проходит по каждой записи в полученном XML со списка, который ЦБ отдает за период.
                for record in records:
                    try:
                        # 1. Проверяем наличие атрибута ID. Извлекает код металла (1-Золото, 2-Серебро и т.д.).
                        raw_code = record.get('Code')
                        if raw_code is None:
                            continue  # Пропускаем, если ID нет.

                        # ID: 1-Золото, 2-Серебро, 3-Платина, 4-Палладий.
                        code = int(raw_code)

                        # 2. Ищет узел с ценой и заменяем запятую на точку для расчетов.
                        buy_node = record.find('Buy')
                        if buy_node is not None and buy_node.text:
                            # Заменяем запятую на точку для перевода в float
                            price = float(buy_node.text.replace(',', '.'))

                            # ЦБ присылает данные за несколько дней.
                            # Собирает ВСЕ цены за период, добавляя цену в список для конкретного металла.
                            if code not in temp_rates:
                                temp_rates[code] = []
                            temp_rates[code].append(price)

                            # После цикла оставьте только последние две цены для каждого металла:
                            self.metal_rates = {k: v[-2:] for k, v in temp_rates.items()}

                    except (ValueError, AttributeError) as e:
                        self.logger.warning(f"⚠️ Пропущена некорректная запись в XML: {e}")
                        continue

                # 5. Сохраняет только две последние цены для расчета динамики (вчера/сегодня).
                self.metal_rates = {k: v[-2:] for k, v in temp_rates.items()}

                self.logger.info(f"✅ Курсы обновлены: {self.metal_rates}")
                return True

            self.logger.error(f"❌ Ошибка ЦБ: статус {response.status_code}. Проверьте URL и заголовки.")
            return False

        except Exception as e:
            self.logger.error(f"❌ Критическая ошибка в metal_api: {e}", exc_info=True)
            return False

    def get_metal_value(self, metal_code: int):
        """
        Возвращает цену за 1 грамм в рублях.
        1 - Золото, 2 - Серебро, 3 - Платина, 4 - Палладий.
        """
        # Возвращает последнюю цену или 0.0, если данных нет.
        prices = self.metal_rates.get(metal_code, [])
        return prices[-1] if prices else 0.0
