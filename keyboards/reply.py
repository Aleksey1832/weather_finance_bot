from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# --- Клавиатуры ---
start_button = KeyboardButton(text='Старт 🏠')
cancel_button = KeyboardButton(text='Отмена ❌')
weather_button_reply = KeyboardButton(text='Погода 🌤')
loc_button = KeyboardButton(text="Отправить локацию 📍", request_location=True)
finance_button = KeyboardButton(text='Курсы валют 📈')

# ReplyKeyboardMarkup для основных действий
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [start_button],
        [cancel_button]
    ],
    resize_keyboard=True,
    one_time_keyboard=False # Клавиатура остается видимой
)

main_keyboard_1 = ReplyKeyboardMarkup(
    keyboard=[
        [start_button],
    ],
    resize_keyboard=True,
    one_time_keyboard=False # Клавиатура остается видимой
)

main_keyboard_2 = ReplyKeyboardMarkup(
    keyboard=[
        [finance_button, weather_button_reply],
        [cancel_button]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите нужный раздел 👇",
    one_time_keyboard=False # Клавиатура остается видимой
)

main_keyboard_3 = ReplyKeyboardMarkup(
    keyboard=[
        [cancel_button],
    ],
    resize_keyboard=True,
    one_time_keyboard=False # Клавиатура остается видимой
)

# Клавиатура, которая выскочит ПОСЛЕ нажатия инлайн-кнопки "По геолокации".
loc_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [loc_button],
        [cancel_button]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите нужный раздел 👇",
    one_time_keyboard=True # Исчезнет после одного нажатия
)
