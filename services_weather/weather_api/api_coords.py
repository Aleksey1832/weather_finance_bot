import logging
import requests
from config.settings import open_weather_token, WEATHER_BASE_URL


def get_weather_by_coords(lat, lon):
    """
    ЗАПРОС ПО КООРДИНАТАМ (lat, lon)
    """
    logger = logging.getLogger(__name__)
    try:
        # 1. Формирование словаря параметров для API-запроса.
        params = {
            "lat": lat,
            "lon": lon,
            "appid": open_weather_token,
            "units": "metric",
            "lang": "ru"
        }

        # 2. Выполнение GET-запроса с ограничением по времени ожидания 10 секунд.
        response = requests.get(WEATHER_BASE_URL, params=params, timeout=10)
        logger.info(f"Ответ по координатам получен. Status code: {response.status_code}")

        # 3. Проверка HTTP-статуса. Генерирует исключение для кодов 4xx и 5xx.
        response.raise_for_status()

        # 4. Преобразование тела ответа из формата JSON в словарь Python.
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        # Обработка ошибок, связанных с некорректными HTTP-статусами (4xx, 5xx).
        logger.error(f"HTTP ошибка при запросе координат {lat}, {lon}: {http_err}")

    except requests.exceptions.ConnectionError as conn_err:
        # Обработка ошибок сетевого подключения или недоступности сервера.
        logger.error(f"Ошибка сетевого соединения: {conn_err}")

    except Exception: # noqa
        # Перехват и логирование любых других непредвиденных исключений со стеком вызовов.
        logger.exception(f"Непредвиденная ошибка GPS-запроса для {lat}, {lon}")

    return None
