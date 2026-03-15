from datetime import datetime, timezone, timedelta


def process_weather_json(data: dict):
    """
    Превращает сырой JSON в словарь с обработанными данными.
    """
    # 1. Безопасно достает основные ветки, чтобы не ловить KeyError.
    main = data.get('main', {})
    sys = data.get('sys', {})
    wind = data.get('wind', {})
    weather_list = data.get('weather', [{}])
    weather_item = weather_list[0] if weather_list else {}

    # 2. Работа с тайм-зоной и временем.
    tz_offset = data.get('timezone', 0)
    city_tz = timezone(timedelta(seconds=tz_offset))

    # 3. Рассвет/закат с защитой от отсутствия данных.
    sr_ts = sys.get('sunrise', 0)
    ss_ts = sys.get('sunset', 0)

    sunrise = datetime.fromtimestamp(sr_ts, tz=city_tz).strftime('%H:%M') if sr_ts else "--:--"
    sunset = datetime.fromtimestamp(ss_ts, tz=city_tz).strftime('%H:%M') if ss_ts else "--:--"

    # 4. Продолжительность дня.
    duration = ss_ts - sr_ts if (ss_ts and sr_ts) else 0
    day_len = f"{duration // 3600}ч. {(duration % 3600) // 60}мин."

    # 5. Направление ветра.
    directions = ["⬇️ С", "↙️ СВ", "⬅️ В", "↖️ ЮВ", "⬆️ Ю", "↗️ ЮЗ", "➡️ З", "↘️ СЗ"]
    wind_deg = wind.get('deg', 0)
    wind_dir = directions[int((wind_deg + 22.5) // 45) % 8]

    # 6. Осадки.
    rain = data.get('rain', {}).get('1h', 0)
    snow = data.get('snow', {}).get('1h', 0)
    precip_text = f"🌧 Дождь: {rain}мм" if rain else (f"❄️ Снег: {snow}мм" if snow else "Без осадков")

    return {
        "city": data.get('name', 'Неизвестно'),
        "temp": round(main.get('temp', 0)),
        "feels_like": round(main.get('feels_like', 0)),
        "pressure": round(main.get('pressure', 0) * 0.75006),
        "humidity": max(0, main.get('humidity', 5) - 5),
        "desc": weather_item.get('description', 'нет описания'),
        "wind_speed": wind.get('speed', 0),
        "wind_dir": wind_dir,
        "wind_gust": wind.get('gust', 'нет'),
        "precip": precip_text,
        "visibility": data.get('visibility', 0) / 1000,
        "sunrise": sunrise,
        "sunset": sunset,
        "day_len": day_len,
    }
