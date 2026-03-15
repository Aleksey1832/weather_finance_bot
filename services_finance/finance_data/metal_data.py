import logging
from datetime import datetime


class MetalFormatter:
    """
    Форматировщик данных по драгметаллам из ЦБ РФ.
    """

    @staticmethod
    def get_metals_report(manager):
        """
        Собирает отчет на основе данных из MetalDataManager.
        """
        logger = logging.getLogger(__name__)

        # Проверяет доступность данных (обновляет через кэш или API)
        if not manager.update_rates():
            logger.warning("Не удалось получить данные для отчета по металлам")
            return "🥇🥈 <b>Металлы:</b> <i>Данные ЦБ временно недоступны</i>"

        def format_row(code, name, icon):
            # Получает список цен [вчера, сегодня] для конкретного металла
            prices = manager.metal_rates.get(code, [])

            # Возвращает заглушку, если данных по коду нет
            if not prices:
                logger.debug(f"Данные по металлу {name} (код {code}) отсутствуют в ответе")
                return f"{icon} <b>{name}:</b> <i>нет данных</i>"

            # Извлекает текущую цену (последний элемент)
            curr = prices[-1]

            # Проверяет наличие минимум двух цен для расчета динамики
            if len(prices) > 1:
                # Извлекает предыдущую цену (предпоследний элемент)
                prev = prices[-2]

                # Защищает от деления на ноль при некорректных данных
                if prev == 0:
                    logger.error(f"Нулевая предыдущая цена для {name}. Расчет процентов невозможен.")
                    return f"{icon} <b>{name}:</b> {curr:,.2f} ₽"

                # Вычисляет разницу в цене и процентное изменение
                change = curr - prev
                pct = (change / prev) * 100

                # Определяет иконку тренда (рост/падение)
                arrow = "📈" if change >= 0 else "📉"

                # Формирует строку с ценой, стрелкой и процентом (с автоматическим знаком +/-).
                return f"{icon} <b>{name}:</b> {curr:,.2f} ₽ {arrow} ({pct:+.2f}%)"

            # Формирует строку только с ценой, если данных для сравнения мало
            return f"{icon} <b>{name}:</b> {curr:,.2f} ₽"

        # Генерирует строки для Золота (код 1) и Серебра (код 2)
        gold_row = format_row(1, "Золото", "🥇")
        silver_row = format_row(2, "Серебро", "🥈")

        # Получает текущую системную дату
        date_str = datetime.now().strftime('%d.%m.%Y')

        # Собирает итоговый текстовый блок для отправки в Telegram
        logger.info("Текстовый блок по металлам успешно сформирован")
        return (
            f"✅ <b>Учетные цены металлов ЦБ РФ</b>\n"
            f"📅 на {date_str} (₽/гр):\n\n"
            f"{gold_row}\n"
            f"{silver_row}\n\n"
            f"⚠️ <i>Динамика к предыдущему торговому дню.</i>"
        )
