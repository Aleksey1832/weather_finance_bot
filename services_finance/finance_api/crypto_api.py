import logging
import requests
from config.settings import coin_api_key, api_crypto


class CryptoDataManager:
    """
        Менеджер поставки данных криптовалют.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api_url = api_crypto
        self.data = {}

    def update_rates(self):
        """Обновление курсов криптовалют."""
        try:
            params = {
                'ids': 'bitcoin,ethereum,dogecoin',
                'vs_currencies': 'usd',
                'precision': '4'
            }
            headers = {
                "accept": "application/json",
                "x-cg-demo-api-key": coin_api_key
            }

            response = requests.get(self.api_url, params=params, headers=headers, timeout=10)
            self.logger.info(f"CoinGecko ответил: {response.status_code} ✅")

            if response.status_code == 200:
                self.data = response.json()
                self.logger.info("✅ Курсы криптовалют успешно обновлены")
            elif response.status_code == 429:
                self.logger.warning("⚠️ CoinGecko: Too Many Requests (429)")
            else:
                self.logger.error(f"❌ Ошибка CoinGecko: {response.status_code}")

        except Exception as e:
            self.logger.error(f"❌ Сервер крипты временно недоступен: {e}")

    def get_price(self, coin_id: str):
        """Возвращает цену конкретной монеты в USD (float) или 0.0"""
        # Достаем цену из вложенного словаря: data['bitcoin']['usd']
        return self.data.get(coin_id, {}).get('usd', 0.0)

    def get_btc(self):
        return self.get_price('bitcoin')

    def get_eth(self):
        return self.get_price('ethereum')

    def get_doge(self):
        return self.get_price('dogecoin')
