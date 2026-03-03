import logging
import requests
from config.settings import open_weather_token, WEATHER_BASE_URL


def get_weather_by_coords(lat, lon):
    """
    ЗАПРОС ПО КООРДИНАТАМ (lat, lon)
    """
    logger = logging.getLogger(__name__)
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": open_weather_token,
            "units": "metric",
            "lang": "ru"
        }

        response = requests.get(WEATHER_BASE_URL, params=params, timeout=10)
        logger.info(f"Ответ по координатам получен. Status code: {response.status_code}")

        return response.json()

    except Exception as e:
        logger.exception(f"Ошибка GPS-запроса: {e}")
        return None
