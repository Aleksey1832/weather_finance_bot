import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import  CallbackQuery
from keyboards.reply import loc_keyboard, main_keyboard_2
from services_weather.weather_api.api_coords import get_weather_by_coords
from services_weather.weather_report.parse_data import format_weather_message


logger = logging.getLogger(__name__)
router = Router()

# Реакция на кнопку location_callback - Inline-кнопки "По геопозиции".
@router.callback_query(F.data == 'location_callback')
async def weather_by_location_handler(callback: CallbackQuery):
    """
    Юзер нажал 'По геопозиции'. Просим его нажать Reply-кнопку.
    """
    logger.info(f"Пользователь {callback.from_user.id} нажал inline-кнопку По геолокации")

    await callback.message.answer(
        "📍 Нажми кнопку «Отправить локацию» ниже.\n\n"
             "⚠️ Примечание: на ПК функция может не работать!",
        reply_markup=loc_keyboard
    )
    await callback.answer()


@router.message(F.location)
async def handle_user_location(message: Message):
    """
    Ловит координаты, когда юзер нажал на кнопку "Отправить локацию"
    """
    logger.info(
        f"Полученное местоположение от пользователя {message.from_user.id}: "
        f"lat={message.location.latitude}, "
        f"lon={message.location.longitude}"
    )

    # 1. Отправляем "часики", чтобы юзер видел, что бот работает.
    wait_msg = await message.answer("📡 Запрашиваю данные со спутников...")

    try:
        # 2. Получает широту и долготу.
        lat = message.location.latitude
        lon = message.location.longitude

        # 3. Вызывает погоду - JSON по координатам.
        weather_dict = get_weather_by_coords(lat, lon)

        # 4. Превращает словарь - JSON в текст вывода.
        result_text = format_weather_message(weather_dict)

        # 5. Защита от пустого ответа.
        if not result_text:
            logger.error(f"Failed to format weather for coords: {lat}, {lon}")
            result_text = "❌ Не удалось определить погоду по вашим координатам."

        # 6. Отправляет ответ и возвращает главное меню.
        await message.answer(result_text, reply_markup=main_keyboard_2)

        # 7. Удаляет временное сообщение "Запрашиваю...".
        await wait_msg.delete()

    except Exception as e:
        logger.exception(f"Ошибка в handle_user_location: {e}")
        await message.answer("❌ Произошла ошибка при получении погоды по GPS.")
