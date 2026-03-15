def get_weather_icon(desc):
    desc = desc.lower()
    # Располагаем более "сильные" погодные явления выше,
    # чтобы 'гроза' победила 'дождь' при поиске подстроки.
    icons = {
        "гроза": "⛈",
        "снег": "❄️",
        "дождь": "🌧",
        "ливень": "🌧",
        "ясно": "☀️",
        "облачно": "☁️",
        "пасмурно": "☁️",
        "туман": "🌫",
        "дымка": "🌫" # OpenWeather любит слово 'дымка'.
    }
    for key, value in icons.items():
        if key in desc:
            return value
    return "🌈" # Если прилетело что-то экзотическое типа "торнадо".

def get_temp_bar(temp):
    if temp < -20: return "🥶 🟦⬜️⬜️⬜️"
    if temp < -10: return "❄️ 🟦🟦⬜️⬜️"
    if temp < 0:   return "🧊 🟦🟦🟦⬜️"
    if temp < 15:  return "🍃 🟩🟩⬜️⬜️"
    if temp < 25:  return "☀️ 🟩🟩🟩⬜️"
    return "🔥 🟥🟥🟥🟥"
