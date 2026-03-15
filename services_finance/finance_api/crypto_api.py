import logging # Импортирует модуль для логирования событий в консоль.
import requests # Импортирует библиотеку для отправки HTTP-запросов к API.
from config.settings import coin_api_key, api_crypto # Загружает ключи и URL из файла настроек.
from utils.cache_manager import finance_cache # Импортирует общий объект кэша (синглтон).


class CryptoDataManager:
    """
        Менеджер поставки данных криптовалют.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__) # Создает логгер с именем текущего модуля.
        self.api_url = api_crypto # Сохраняет базовый URL API CoinGecko.
        self.cache = finance_cache  # # Подключает ссылку на общий механизм кэширования.
        self.crypto_rates = {} # Инициализирует пустой словарь для хранения текущих курсов.

    def update_rates(self):
        """Обновление курсов криптовалют."""
        # 1. Проверяет кэш по ключу "crypto_rates".
        cached_val = self.cache.get("crypto_rates")

        # 2. Если данные в кэше есть и они не устарели (TTL).
        if cached_val:
            self.crypto_rates = cached_val # Записывает данные из кэша в текущую переменную.
            self.logger.info("📦 Криптовалюты взяты из кэша")
            return True # Подтверждает успешное обновление.

        try:
            # 3. Подготавливает параметры запроса: какие монеты, в какой валюте и точность.
            params = {
                'ids': 'bitcoin,ethereum,dogecoin',
                'vs_currencies': 'usd',
                'precision': '4'
            }
            # 4. Устанавливает заголовки, включая API-ключ для авторизации на CoinGecko.
            headers = {
                "accept": "application/json",
                "x-cg-demo-api-key": coin_api_key
            }

            # 5. Выполняет GET-запрос к API с тайм-аутом ожидания 10 секунд.
            response = requests.get(self.api_url, params=params, headers=headers, timeout=10)
            self.logger.info(f"CoinGecko ответил: {response.status_code} ✅")

            # 6. Если запрос прошел успешно (статус 200).
            if response.status_code == 200:
                data = response.json() # Преобразует JSON-ответ в Python-словарь.
                if data:
                    self.crypto_rates = data # Сохраняет данные в оперативную память объекта.
                    self.cache.set("crypto_rates", data) # Записывает свежие данные в кэш.
                    self.logger.info("✅ Курсы криптовалют успешно обновлены")
                    return True # Возвращает подтверждение успеха.

            elif response.status_code == 429: # Если превышен лимит запросов (ошибка 429).
                self.logger.warning("⚠️ CoinGecko: Too Many Requests (429)")
            else:
                self.logger.error(f"❌ Ошибка CoinGecko: {response.status_code}")
                return False # Возвращает статус неудачи.

        except Exception as e: # Обрабатывает любые сетевые сбои или ошибки парсинга.
            self.logger.error(f"❌ Сервер крипты временно недоступен: {e}")
            return False # Возвращает статус неудачи.

    def get_price(self, coin_id: str):
        """Возвращает цену конкретной монеты в USD (float) или 0.0"""
        # Достаем цену из вложенного словаря: data['Bitcoin']['usd'].
        # Безопасно извлекает цену из вложенного словаря: сначала монету, потом поле 'usd'.
        return self.crypto_rates.get(coin_id, {}).get('usd', 0.0)

    # Обертки для удобного получения цены Bitcoin, Ethereum, Dogecoin.
    def get_btc(self):
        return self.get_price('bitcoin')

    def get_eth(self):
        return self.get_price('ethereum')

    def get_doge(self):
        return self.get_price('dogecoin')
