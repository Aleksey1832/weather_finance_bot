def get_weather_icon(desc):
    desc = desc.lower()
    icons = {
        "ясно": "☀️",
        "облачно": "☁️",
        "пасмурно": "☁️",
        "дождь": "🌧",
        "снег": "❄️",
        "гроза": "⛈",
        "туман": "🌫"
    }
    for key, value in icons.items():
        if key in desc:
            return value
    return "🌈"

def get_temp_bar(temp):
    if temp < -20: return "🥶 🟦⬜️⬜️⬜️"
    if temp < -10: return "❄️ 🟦🟦⬜️⬜️"
    if temp < 0:   return "🧊 🟦🟦🟦⬜️"
    if temp < 15:  return "🍃 🟩🟩⬜️⬜️"
    if temp < 25:  return "☀️ 🟩🟩🟩⬜️"
    return "🔥 🟥🟥🟥🟥"
