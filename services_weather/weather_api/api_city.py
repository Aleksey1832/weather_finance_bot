import logging
import requests
from config.settings import open_weather_token, WEATHER_BASE_URL


def get_weather_by_city(city_name):
    """
    Запрос по городу.
    """
    logger = logging.getLogger(__name__)
    try:
        # 1. Формирование параметров словаря params с названием города,
        # API-ключом и настройками формата (метрическая система, русский язык).
        params = {
            "q": city_name,
            "appid": open_weather_token,
            "units": "metric",
            "lang": "ru"
        }

        # 2. Выполнение GET-запроса.
        response = requests.get(WEATHER_BASE_URL, params=params, timeout=10)
        logger.info(f"Ответ но названию города получен. Status code: {response.status_code}")

        # 3. Проверка HTTP-статуса. Генерирует исключение для кодов 4xx и 5xx.
        response.raise_for_status()

        logger.info(f"Ответ но названию города получен. Status code: {response.status_code}")

        # 4. Десериализация JSON в словарь.
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP ошибка: {http_err}")
    except requests.exceptions.ConnectionError as errc:
        logger.error(f"Ошибка соединения: {errc}")
    except Exception: # noqa
        logger.exception(f"Ошибка запроса города:")

    return None
