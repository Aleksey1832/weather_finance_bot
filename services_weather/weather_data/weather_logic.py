from datetime import datetime, timezone, timedelta


def process_weather_json(data: dict):
    """
    Превращает сырой JSON в словарь с обработанными данными.
    """
    tz_offset = data.get('timezone', 0)
    city_tz = timezone(timedelta(seconds=tz_offset))

    sunrise = datetime.fromtimestamp(data['sys']['sunrise'], tz=city_tz).strftime('%H:%M')
    sunset = datetime.fromtimestamp(data['sys']['sunset'], tz=city_tz).strftime('%H:%M')

    # Продолжительность дня (здесь пояс не нужен, это просто разница).
    duration = data['sys']['sunset'] - data['sys']['sunrise']
    day_len = f"{duration // 3600}ч. {(duration % 3600) // 60}мин."

    # Направление ветра.
    directions = ["⬇️ С", "↙️ СВ", "⬅️ В", "↖️ ЮВ", "⬆️ Ю", "↗️ ЮЗ", "➡️ З", "↘️ СЗ"]
    wind_deg = data['wind'].get('deg', 0)
    wind_dir = directions[int((wind_deg + 22.5) // 45) % 8]

    # Влажность, осадки.
    raw_humidity = data['main'].get('humidity', 0)
    rain = data.get('rain', {}).get('1h', 0)
    snow = data.get('snow', {}).get('1h', 0)

    # Формирование переменной осадки.
    precip_text = f"🌧 Дождь: {rain}мм" if rain else (f"❄️ Снег: {snow}мм" if snow else "Без осадков")

    return {
        "city": data.get('name'),
        "temp": round(data['main']['temp']),
        "feels_like": round(data['main']['feels_like']),
        "pressure": round(data['main']['pressure'] * 0.75006),
        "humidity": max(0, raw_humidity - 5),
        "desc": data['weather'][0]['description'],
        "wind_speed": data['wind'].get('speed', 0),
        "wind_dir": wind_dir,
        "wind_gust": data['wind'].get('gust', 'нет'),
        "rain": data.get('rain', {}).get('1h', 0),
        "snow": data.get('snow', {}).get('1h', 0),
        "precip": precip_text,
        "directions": directions,
        "visibility": data.get('visibility', 0) / 1000,
        "sunrise": sunrise,
        "sunset": sunset,
        "day_len": day_len,
    }
