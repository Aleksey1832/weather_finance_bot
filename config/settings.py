import os
from dotenv import load_dotenv


load_dotenv()

# Уровень логирования в файл bot_logs.log.
LOGGER_LEVEL_FILE = "ERROR"
LOGGER_LEVEL_CONSOLE = "INFO"

open_weather_token = os.getenv("OPEN_WEATHER_TOKEN")
open_bot_token = os.getenv("OPEN_BOT_TOKEN")
coin_api_key = os.getenv("COIN_API_KEY")
api_currency = os.getenv("API_CURRENCY")
api_crypto = os.getenv("API_CRYPTO")
api_metals = os.getenv("API_METALS")

REQUIRED_CURRENCIES = ['USD', 'EUR','CZK']
REQUIRED_CRYPTS = ['bitcoin', 'ethereum', 'dogecoin']

# Иконки для crypto_data.py.
ICONS = {
    'bitcoin': '🅱️',
    'ethereum': '💎',
    'dogecoin': '🐕'
}

# Ссылка для api_coords.py поиск погоды по координатам геолокации,
# и api_city.py поиск погоды по названию города.
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Ссылка на канал при подписке (переброска на канал админа).
link_to_channel = os.getenv("LINK_TO_CHANNEL")
raw_channel_id = os.getenv("CHANNEL_ID")
