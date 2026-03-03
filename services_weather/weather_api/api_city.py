import logging
import requests
from config.settings import open_weather_token, WEATHER_BASE_URL


def get_weather_by_city(city_name):
    """
    Запрос по городу.
    """
    logger = logging.getLogger(__name__)
    try:
        params = {
            "q": city_name,
            "appid": open_weather_token,
            "units": "metric",
            "lang": "ru"
        }

        response = requests.get(WEATHER_BASE_URL, params=params, timeout=10)
        logger.info(f"Ответ но названию города получен. Status code: {response.status_code}")

        return response.json()

    except Exception as e:
        logger.exception(f"Ошибка запроса города: {e}")
        return None
