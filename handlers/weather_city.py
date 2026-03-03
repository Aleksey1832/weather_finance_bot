import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from services_weather.weather_report.parse_data import format_weather_message
from services_weather.weather_api.api_city import get_weather_by_city
from keyboards.inline import weather_inline_markup
from keyboards.reply import main_keyboard_2, main_keyboard_3
from utils.states import WeatherStates


logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text.casefold().in_({"погода", "погода 🌤", "/weather"}))
async def weather_reply_button_handler(message: Message):
    """
    Обработчик нажатия на кнопку "Погода" на клавиатуре ReplyKeyboardMarkup.
    Предлагает выбор способа получения погоды.
    """
    # Логирование, что юзер нажал на главную кнопку.
    logger.info(f"Пользователь {message.from_user.id} нажал на главную кнопку Погода")

    await message.answer(
        "Как вы хотите узнать погоду?",
        reply_markup=weather_inline_markup # Отображение инлайн-выбора (Город или GPS).
    )

    await message.answer(
        "Вы можете отменить выбор, нажав кнопку ниже 👇",
        reply_markup=main_keyboard_3
    )

# --- Обработчик CallbackQuery (для Inline кнопок) ---

# 1. При клике на кнопку включаем состояние ожидания FSM.
@router.callback_query(F.data == 'weather_callback')
async def weather_callback_handler(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия на Inline кнопку "Погода".
    """
    # Логирование входа в режим ожидания.
    logger.info(f"Пользователь {callback.from_user.id} запустил прогноз погоды FSM (wait_city)")

    try:
        await callback.message.answer("Введите название города, чтобы узнать погоду:")
        await state.set_state(WeatherStates.wait_city)  # Бот теперь "ждет" город.
        await callback.answer() # Отвечает на callback query, чтобы убрать часики.

    except Exception as e:
        logger.debug(f"Не удалось получить ответ на обратный вызов (обычно для старых запросов): {e}")

# 2. Работает, если бот находится в состоянии wait_city.
@router.message(WeatherStates.wait_city, F.text)
async def process_city_input(message: Message, state: FSMContext):
    """
        Ловит сообщение - название города.
    """
    # 1. Получает данные из нашего сервиса.
    city_name = message.text.strip()

    # Логирование, какой город ввел юзер.
    logger.info(f"Пользователь {message.from_user.id} ввел город: {city_name}")

    try:
        # 2. Вызывает погоду - JSON по названию города.
        weather_dict = get_weather_by_city(city_name)

        # Если API совсем не ответило (None).
        if weather_dict is None:
            logger.error(f"API вернуло None для города: {city_name}")
            await message.answer("📡 Ошибка связи с сервером погоды. Попробуйте позже.")
            await state.clear()
            return

        # 2.1 Превращает словарь - JSON в текст вывода.
        result_text = format_weather_message(weather_dict)

        if not result_text:
            # Если функция вернула None или пустую строку.
            logger.warning(f"Город не найден или результат пустой: {city_name}")
            result_text = (f"❌ Город «{city_name}» не найден.\n"
                           f"Вы уверены, что он на Земле?\n"
                           f"Проверьте правильность написания.")

        # 2.2 Отправка пользователю готового ответа.
        await message.answer(result_text)

        # Логирование успешного завершения.
        logger.info(f"Погода для {city_name} успешно отправлена пользователю {message.from_user.id}")

    except Exception as e:
        logger.exception(f"Непредвиденная ошибка в обработчике погоды: {e}")
        await message.answer("❌ Произошла техническая ошибка.")

    finally:
        # 3. Предложение помощи в очищенном состоянии.
        await message.answer(
            f"<b>Чем еще могу помочь?\n\n</b>"
            f"<b>Выбери кнопки:\n«Курсы валют 📈» или «Погода 🌤» ниже.</b>",
            reply_markup=main_keyboard_2
        )
        await state.clear()

# 3. Финальный хендлер - заглушка.
@router.message(WeatherStates.wait_city)
async def process_unknown_input(message: Message):
    """
    Сработает на всё, что не является текстом (фото, стикеры)
    или на текст, если мы не вышли из состояния.
    """
    # Логируем, если юзер прислал стикер или фото вместо текста.
    logger.info(f"Пользователь {message.from_user.id} отправил нетекстовый контент в wait_city: {message.content_type}")

    await message.answer(
        "Хьюстон, у нас проблемы! 🛰\n"
        "Я жду название города. Если передумал — нажми кнопку «Отмена ❌»."
    )
