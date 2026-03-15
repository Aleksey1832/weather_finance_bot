import logging
from aiogram import Bot
from config.settings import raw_channel_id
from aiogram.enums import ChatMemberStatus

logger = logging.getLogger(__name__)

CHANNEL_ID = int(raw_channel_id)  # ID канала (обязательно с -100)

async def is_user_subscribed(bot: Bot, user_id: int) -> bool:
    """Проверяет, подписан ли юзер на наш канал."""
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        # Если юзер не 'left', не 'kicked' и не 'restricted'.
        return member.status not in {ChatMemberStatus.LEFT, ChatMemberStatus.KICKED}

    except Exception as e:
        logger.error(f"Ошибка при допросе Telegram: {e}")
        return False
