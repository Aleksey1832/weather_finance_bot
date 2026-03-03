import asyncio
import logging
from config.logger_setup import setup_logger
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from config.settings import open_bot_token
from handlers import common, weather_city, weather_location, finance_router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


# Настройка логирования, чтобы знать, если бот решит "приуныть".
# logging.basicConfig(
#     level=logging.ERROR,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )
setup_logger()
logger = logging.getLogger(__name__)

async def main():
    session = AiohttpSession(timeout=40)
    # Инициализация бота.
    bot = Bot(
        token=open_bot_token,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Подключение модулей (роутеров).
    # Порядок важен! Если common.py ловит всё подряд, нужно ставить его ниже.
    dp.include_router(finance_router.router)
    dp.include_router(weather_city.router)
    dp.include_router(weather_location.router)
    dp.include_router(common.router)

    logger.info("🤖 Бот успешно запущен!")

    try:
        # Запуск бесконечного цикла опроса серверов Telegram.
        # Удаляет все накопленные сообщения, пока бот спал (drop_pending_updates=True).
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    except Exception as e:
        logger.exception(f"Не удалось удалить вебхук при старте (проблема с сетью): {e}")

    finally:
        await bot.session.close()  # ЗАКРЫВАЕМ СЕССИЮ ПРИ ВЫКЛЮЧЕНИИ.
        logger.info("🔌 Сессия бота закрыта.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🔌 Бот выключен.")
