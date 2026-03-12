import logging
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
    file_handler.setLevel(logging.ERROR)  # В файл пишем только ОШИБКИ.

    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.INFO)  # В консоль пишем ИНФО и ошибки.

    # Настройка корневого логгера
    root_logger = logging.getLogger()
    # Чистим старые хендлеры, если они были (защита от дубликатов при перезагрузке)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
