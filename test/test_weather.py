import pytest
from services_weather.weather_data.weather_logic import process_weather_json


def test_process_weather_json_valid_data():
    """
    Тест: Проверяем, что функция правильно парсит нормальный ответ API.
    """
    mock_data = {
        "name": "Москва",
        "main": {"temp": 10.6, "feels_like": 8.2, "pressure": 1013, "humidity": 60},
        "weather": [{"description": "ясно"}],
        "wind": {"speed": 5, "deg": 0},
        "sys": {"sunrise": 1715824800, "sunset": 1715882400},
        "timezone": 10800,
        "visibility": 10000,
        "cod": 200
    }

    result = process_weather_json(mock_data)

    # Проверяем ключевые поля
    assert result["city"] == "Москва"
    assert result["temp"] == 11  # round(10.5)
    assert result["pressure"] == 760  # 1013 * 0.75006
    assert result["wind_dir"] == "⬇️ С"
    assert "ч." in result["day_len"]


def test_process_weather_json_empty_data():
    """
    Тест: Проверяем выживаемость функции при пустом словаре (защита от KeyError).
    """
    empty_data = {}

    # Если мы всё сделали правильно с .get(), функция не должна упасть
    result = process_weather_json(empty_data)

    assert result["city"] == "Неизвестно"
    assert result["temp"] == 0
    assert result["desc"] == "нет описания"
