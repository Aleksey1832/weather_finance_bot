import logging
import requests
from config.settings import api_currency
from utils.cache_manager import finance_cache


class CurrencyDataManager:
    """
    Менеджер поставки данных курса валют.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api_url = api_currency
        self.cache = finance_cache  # Использует общий кэш.
        self.currency_rates = {}

    def update_rates(self):
        """Загрузка данных из ЦБ РФ."""
        # 1. Проверяет кэш.
        cached_val = self.cache.get("currency_rates")
        if cached_val:
            self.currency_rates = cached_val
            self.logger.info("📦 Валюта взята из кэша")
            return True

        try:
            # 2. Выполняет запрос к серверу ЦБ с ограничением ожидания 5 секунд.
            response = requests.get(self.api_url, timeout=5)
            self.logger.info(f"ЦБ РФ ответил: {response.status_code} ✅")

            # 3. Проверяет успешность HTTP-статуса (200 OK).
            if response.status_code == 200:
                # 4. Преобразует JSON-ответ от ЦБ в словарь Python.
                data = response.json()
                # 5. Сохраняет весь словарь 'Valute', USD и EUR со всеми полями.
                self.currency_rates = data.get('Valute', {})
                # 6. Сохраняет в кеш свежие данные.
                self.cache.set("currency_rates", self.currency_rates)

                self.logger.info("✅ Данные ЦБ успешно получены")
                self.logger.debug(f"DEBUG: Ключи в rates: {list(self.currency_rates.keys())}")
                self.logger.debug(data)
                return True

            return False

        except Exception as e:
            # 7. Перехватывает ошибки сети или сбои сервера ЦБ, чтобы бот не упал.
            self.logger.error(f"❌ Сервер ЦБ временно недоступен: {e}")
            return False

    def get_currency_data(self, code: str):
        """
        Возвращает полный словарь по коду валюты (USD, EUR, CZK и т.д.)
        Там будут поля: 'Value', 'Previous', 'Name'.
        """
        return self.currency_rates.get(code, {})

    # Методы для совместимости (если они нужны в других местах).
    def get_usd_value(self):
        """Возвращает цену 1 доллара в рублях"""
        usd_data = self.currency_rates.get('USD')
        self.logger.debug(f"DEBUG ВНУТРИ КЛАССА: Данные USD: {usd_data}")

        if usd_data:
            val = usd_data.get('Value', 0.0)
            self.logger.debug(f"DEBUG ВНУТРИ КЛАССА: Достали Value: {val}")
            return val
        return 0.0

    def get_eur_value(self):
        """Возвращает цену 1 евро в рублях"""
        eur_data = self.currency_rates.get('EUR')
        self.logger.debug(f"DEBUG ВНУТРИ КЛАССА: Данные EUR: {eur_data}")

        if eur_data:
            val = eur_data.get('Value', 0.0)
            self.logger.debug(f"DEBUG ВНУТРИ КЛАССА: Достали Value: {val}")
            return val
        return 0.0

    def get_czk_value(self):
        """Возвращает цену 1 чешской кроны в рублях"""
        czk_data = self.currency_rates.get('CZK')
        self.logger.debug(f"DEBUG ВНУТРИ КЛАССА: Данные CZK: {czk_data}")

        if czk_data:
            val = czk_data.get('Value', 0.0)
            self.logger.debug(f"DEBUG ВНУТРИ КЛАССА: Достали Value: {val}")
            return val
        return 0.0
