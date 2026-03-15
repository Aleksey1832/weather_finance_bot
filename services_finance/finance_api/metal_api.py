import logging
import requests
import xml.etree.ElementTree as et
from datetime import datetime, timedelta
from config.settings import api_metals
from utils.cache_manager import finance_cache


class MetalDataManager:
    """
    Менеджер поставки данных по драгметаллам из ЦБ РФ.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api_url = api_metals
        self.cache = finance_cache  # Использует общий кэш.
        self.metal_rates = {}  # Здесь храниться: {1: Золото, 2: Серебро}.

    def update_rates(self):
        # 1. Проверяет кэш.
        cached_val = self.cache.get("metal_rates")
        if cached_val:
            self.metal_rates = cached_val
            self.logger.info("📦 Металлы взяты из кэша")
            return True

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

            # 4. Проверяет статус.
            if response.status_code == 200 and response.content:
                # 4.1 Парсит XML. Превращает XML-текст в дерево объектов.
                root = et.fromstring(response.content)
                temp_rates = {}
                records = root.findall('Record')

                # Печатает кусочек XML для проверки.
                self.logger.debug(f"XML фрагмент: {response.text[:100]}")

                if not records:
                    self.logger.warning("⚠️ В XML нет тегов <Record>. Возможно, праздники или нет торгов.")
                    return False

                # 4.2 Проходит по каждой записи в полученном XML со списка, который ЦБ отдает за период.
                for record in records:
                    try:
                        # 1. Проверяем наличие атрибута ID. Извлекает код металла (1-Золото, 2-Серебро и т.д.).
                        raw_code = record.get('Code')

                        if not raw_code: continue

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

                    except (ValueError, AttributeError) as e:
                        self.logger.warning(f"⚠️ Пропущена некорректная запись в XML: {e}")
                        continue

                # 2. Очищаем данные: оставляем только 2 последние цены для динамики
                processed_rates = {}
                for code, prices in temp_rates.items():
                    # Если цен несколько, берем последние две, если одна — дублируем её
                    if len(prices) >= 2:
                        processed_rates[code] = prices[-2:]
                    elif len(prices) == 1:
                        processed_rates[code] = [prices[0], prices[0]]

                if processed_rates:
                    self.metal_rates = processed_rates
                    # 3. Сохраняем в кэш
                    self.cache.set("metal_rates", processed_rates)
                    self.logger.info(f"✅ Курсы металлов обновлены: {self.metal_rates}")
                    return True

            self.logger.error(f"❌ Ошибка ЦБ: статус {response.status_code}. Проверьте URL и заголовки.")
            return False

        except Exception as e:
            self.logger.error(f"❌ Критическая ошибка в metal_api: {e}", exc_info=True)
            return False

    def get_metal_value(self, metal_code: int):
        """
        Возвращает список [вчерашняя_цена, сегодняшняя_цена] или [0, 0].
        Возвращает цену за 1 грамм в рублях.
        1 - Золото, 2 - Серебро, 3 - Платина, 4 - Палладий.
        """
        # Вернет именно тот список из двух цен, который положен в словарь.
        return self.metal_rates.get(metal_code, [0.0, 0.0])
