import logging
from aiogram.enums import ChatType
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from keyboards.inline import subscription_inline_markup
from keyboards.reply import main_keyboard, main_keyboard_1, main_keyboard_2
from utils.filters import is_user_subscribed


logger = logging.getLogger(__name__)
router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE) # Будут срабатывать только в личных сообщениях.

# --- Обработчики сообщений ---
# 1. Обработчик команды /start.
@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext, bot: Bot):
    """
    Предлагает приветствие, краткое описание бота и варианты действий.
    """
    await state.clear() # Очищаем предыдущее состояние, если оно было.

    if not await is_user_subscribed(bot, message.from_user.id):
        return await message.answer(
            "Вход только для своих! ✋\nСначала подпишитесь на канал.",
            reply_markup=subscription_inline_markup # Отправляем инлайн клавиатуру.
        )

    return await message.answer(
        "Привет! Я бот, который поможет тебе узнать\nкурс валют или прогноз погоды.\n"
        "Нажми на кнопку\n«Курсы валют 📈» или «Погода 🌤» ниже. 👇",
        reply_markup=main_keyboard_2 # Отправляем основную клавиатуру.
    )


# 1.1 Обработка нажатия на кнопку "Я всё сделал!"
@router.callback_query(F.data == "check_sub")
async def check_sub_callback(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id

    # 1. Сначала проверяет подписку (ошибки внутри логируются через logger.exception).
    is_subscribed = await is_user_subscribed(bot, user_id)

    if is_subscribed:
        logger.info(f"Юзер {user_id} успешно подписался! 🎉")
        # Отвечает на кнопку (убирает часики) и пишет сообщение.
        await callback.answer("Подписка подтверждена! ✅")

        # Удаляет старое сообщение с инлайн-кнопкой.
        try:
            await callback.message.delete()

        except Exception as e:
            logger.warning(f"Не удалось удалить сообщение для {user_id} (возможно, оно слишком старое) {e}")

        await callback.message.answer(
            "Вы успешно подписаны на канал! 🚀",
            reply_markup=main_keyboard_1
        )

    else:
        # 2. Если не подписан, показывает всплывающее окно (alert).
        try:
            await callback.answer("Вы все еще не подписаны! 🤨", show_alert=True)
        except Exception as e:
            logger.exception(f"Не удалось отправить alert юзеру {user_id} (кнопка протухла) {e}")
            await callback.message.answer("Подписки нет! 👀")


# 2. Обработчик текстового сообщения "Старт".
@router.message(F.text.casefold().in_({"старт", "старт 🏠", "/start"}))
async def start_text_handler(message: Message, state: FSMContext, bot: Bot):
    """
    Обработчик реагирует на текстовое сообщение "Старт",
    если пользователь нажмет на кнопку "Старт" на клавиатуре ReplyKeyboardMarkup.
    Перезапускает приветствие.
    """
    await command_start_handler(message, state, bot) # Повторно вызывает логику команды /start.

# 3. Обработчик команды /cancel.
@router.message(Command('cancel'))
async def command_cancel_handler(message: Message, state: FSMContext):
    """
    Прерывает текущий диалог и предлагает начать заново.
    """
    current_state = await state.get_state()
    if current_state is None:
        # Логируем, что юзер нажал отмену, когда и так ничего не происходило.
        logger.info(f"Юзер {message.from_user.id} попытался отменить, но состояние было уже пустым.")
        await message.reply("Для начала работы бота нажмите «Старт 🏠».", reply_markup=main_keyboard_1)
        return

    # Логируем, какое именно состояние юзер прерывает.
    logger.info(f"User {message.from_user.id} cancelled state: {current_state}")
    await state.clear()

    await message.answer(
        "Фух, отмена так отмена. Я всё забыл!",
        reply_markup=main_keyboard
    )

    # Удаление инлайн-кнопки, которые висят выше:
    try:
        # Удаление кнопки под последним сообщением.
        await message.edit_reply_markup(reply_markup=None)
    except Exception as e:
        # Logger запишет, почему не удалось убрать кнопки (например, сообщение слишком старое).
        logger.warning(f"Не удалось обработать ответ от пользователя! {message.from_user.id}: {e}")
        await message.reply('Упс. Попробуйте еще раз!')


# 4. Обработчик текстового сообщения "Отмена".
@router.message(F.text.casefold().in_({"отмена", "отмена ❌", "/cancel"}))
async def cancel_text_handler(message: Message, state: FSMContext):
    """
    Реагировать на текстовое сообщение "Отмена",
    если пользователь нажмет на кнопку "Отмена" на клавиатуре ReplyKeyboardMarkup.
    Перенаправляет на логику команды /cancel.
    """
    await command_cancel_handler(message, state)


# 6. Обработчик других команд, кроме (старт, отмена, курс валют, погода).
@router.message()
async def unknown_message(message: Message):
    """
    Сюда попадет всё, что не 'старт', не 'отмена', не курс и не 'погода'
    (потому что роутер погоды мы подключим раньше).
    """
    content_type = message.content_type
    input_text = message.text if message.text else "[not text]"

    logger.info(f"Unknown message from {message.from_user.id}: {input_text} (Type: {content_type})")

    await message.answer(
        "Я тебя не понимаю... 🤔\n\n"
        "Используй кнопки:\n" 
        "«Старт 🏠» или «Отмена ❌»",
        reply_markup=main_keyboard  # Возвращаем основную клавиатуру
    )
