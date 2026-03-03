import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    # Создаем форматтер.
    log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Файловый обработчик с ротацией.
    file_handler = RotatingFileHandler(
        "bot_logs.log",
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
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
