import logging
from config.settings import LOGGER_LEVEL_FILE, LOGGER_LEVEL_CONSOLE
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger():
    # 1. Определяем корень проекта (выходим из config/ на уровень выше)
    base_dir = Path(__file__).resolve().parent.parent
    log_dir = base_dir / "logs"

    # 2. Создаем папку logs, если её нет
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)

    # Путь к файлу теперь всегда будет /home/user/your_bot/logs/bot_logs.log
    log_file_path = log_dir / "bot_logs.log"

    # Создаем форматтер.
    log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Файловый обработчик с ротацией.
    file_handler = RotatingFileHandler(
        log_file_path,  # Используем абсолютный путь.
        maxBytes=10 * 1024 * 1024,  # 10 МБ.
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(log_format)
    file_level = logging.getLevelName(LOGGER_LEVEL_FILE)
    file_handler.setLevel(file_level)  # В файл пишем только ОШИБКИ.

    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_level = logging.getLevelName(LOGGER_LEVEL_CONSOLE)
    console_handler.setLevel(console_level) # В консоль пишем ИНФО и ошибки.

    # 1. Получает объект корневого логгера.
    root_logger = logging.getLogger()

    # 2. Чистит старые хендлеры, если они были (защита от дубликатов при перезагрузке).
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # 3. Устанавливает минимальный общий порог.
    root_logger.setLevel(logging.DEBUG)

    # 4. Настроенные ранее хендлеры.
    root_logger.addHandler(file_handler) # Он будет писать только ERROR (как в настройках).
    root_logger.addHandler(console_handler) # Он будет писать INFO и ERROR.
