from config.settings import link_to_channel
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# --- Клавиатуры ---
# 1. Создание кнопок InlineKeyboardMarkup для подписки или подписался.
subscription_inline_button = InlineKeyboardButton(
    text="Подписаться 📢",
    url = link_to_channel  # Ссылка на канал.
)

subscribed_inline_button = InlineKeyboardButton(
    text="Я подписан! ✅",
    callback_data="check_sub"
)

# 1.1 Собирает кнопки подписки в список списков (каждый внутренний список [] — это новая строка).
subscription_inline_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [subscription_inline_button],
        [subscribed_inline_button]
    ]
)

# 2. Создание кнопок InlineKeyboardMarkup для предложений погоды.
weather_inline_button = InlineKeyboardButton(
    text="🏙 По названию города",
    callback_data="weather_callback"
)

location_inline_button = InlineKeyboardButton(
    text="📍 По геопозиции",
    callback_data="location_callback"
)

# 2.1 Собирает кнопки погоды в список списков (каждый внутренний список [] — это новая строка).
weather_inline_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [weather_inline_button],
        [location_inline_button]
    ]
)
