import logging
from aiogram import Router, F
from aiogram.types import Message
from services_finance.finance_report.parse_data_finance import get_full_finance_report
from keyboards.reply import main_keyboard_2


logger = logging.getLogger(__name__)

router = Router()

# __Обработчик "Курс валют"__
@router.message(F.text == 'Курсы валют 📈')
async def show_finance(message: Message):
    # Логер, кто запросил финансы (для статистики).
    logger.info(f"Юзер {message.from_user.id} запросил финансовый отчет.")

    # 1. Бот может "задуматься" на секунду, пока качает данные.
    wait_message = await message.answer("⏳ Собираю данные с бирж, секунду...")
    try:
        # 1.1 Вызов функции-агрегатор.
        report = get_full_finance_report()

        # 1.2 Отправка отчета (удаляя или просто отвечая новым).
        await message.answer(report)

    # Логируем ошибку с подробностями (traceback).
    except Exception as e:
        logger.exception(f"Критический сбой в finance_router: {e}")
        await message.answer(
            "❌ Не удалось получить данные из-за технического сбоя. Попробуйте позже.",
            reply_markup=main_keyboard_2
        )

    finally:
        # 4. Блок finally выполнится ВСЕГДА (и при успехе, и при ошибке).
        # Часики удалятся в любом случае.
        try:
            await wait_message.delete()
        except Exception as delete_error:
            logger.warning(f"Не удалось удалить wait_message: {delete_error}")

        # 5. В конце предложение помощи.
    await message.answer(
        "<b>Чем еще могу помочь?\n</b>"
        "<b>Выбери кнопки:\n«Курсы валют 📈» или «Погода 🌤» ниже.</b>",
        reply_markup=main_keyboard_2
    )
