from aiogram import Router, F
from aiogram.types import Message
from services_weather.weather_api.api_coords import get_weather_by_coords
from keyboards.reply import main_keyboard
from keyboards.inline import weather_inline_markup
import logging


router = Router()

@router.message(F.location)
async def handle_user_location(message: Message):
    """
    Ловит координаты, когда юзер нажал на кнопку "Отправить локацию"
    """
    logger = logging.getLogger(__name__)
    wait_msg = await message.answer("📡 Связываюсь со спутником...")
    try:
        # Получает широту и долготу.
        lat = message.location.latitude
        lon = message.location.longitude
        logger.info(f"lat и lon получены. {lat}, {lon}")

        # Вызывает погоду - JSON по координатам.
        weather_dict = get_weather_by_coords(lat, lon)

        # Превращает JSON в красивый текст.
        await message.answer(weather_dict, reply_markup=main_keyboard)
        await wait_msg.delete()


    except Exception as e:
        logger.exception(f"Ошибка в обработчике локации: {e}")

        # Если ошибка, предлагаем попробовать еще раз через инлайн-кнопку
        await message.answer(
            "❌ Не удалось определить погоду по GPS.\nПопробуйте нажать кнопку еще раз:",
            reply_markup=weather_inline_markup
        )
