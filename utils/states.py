from aiogram.fsm.state import StatesGroup, State

class WeatherStates(StatesGroup):
    """
    Включение памяти бота при котором он ждет введения города,
    режим ожидания города (wait_city).
    """
    wait_city = State()  # Состояние: "Бот ждет ввода города"
