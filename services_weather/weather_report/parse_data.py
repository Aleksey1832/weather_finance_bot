import logging
from services_weather.weather_data.weather_logic import process_weather_json
from utils.weather_utils import get_weather_icon, get_temp_bar


def format_weather_message(data: dict):
    """
    Собирает текст на вывод погоды.
    """
    logger = logging.getLogger(__name__)

    if data.get("cod") != 200:
        logger.info("Город не найден или API капризничает. 🤷‍")
        return None

    w_dict = process_weather_json(data)  # Получаем обработанные данные
    icon = get_weather_icon(w_dict['desc'])
    bar = get_temp_bar(w_dict['temp'])

    return (
        f"<b>📍 Погода в {w_dict['city']}:</b>\n"
        f"━━━━━━━━━━━━━━━\n"
        f"{icon} <b>{w_dict['desc'].capitalize()}</b>\n"
        f"🌡 <b>Температура: {w_dict['temp']}°C\n</b>"
        f"🤔 <b>Ощущается как: {w_dict['feels_like']}°C\n</b>"
        f"📊 {bar}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🏟 Давление: {w_dict['pressure']} мм рт. ст.\n"
        f"💦 Влажность: {w_dict['humidity']}%\n"
        f"💧 Осадки: {w_dict['precip']}\n"
        f"👀 Видимость: {w_dict['visibility']} км\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💨 Ветер: {w_dict['wind_speed']} м/с ({w_dict['wind_dir']})\n"
        f"🌪 Порывы ветра: {w_dict['wind_gust']} м/с\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🌅 Рассвет: {w_dict['sunrise']}\n"
        f"🌇 Закат: {w_dict['sunset']}\n"
        f"⏱ Долгота дня: {w_dict['day_len']}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"✨ <i> Хорошего дня!</i>"
    )
