from datetime import datetime
from services_finance.finance_api.metal_api import MetalDataManager


class MetalFormatter:
    """
    Форматировщик данных по драгметаллам из ЦБ РФ.
    """

    @staticmethod
    def get_metals_report():
        """
        Собирает отчет на основе данных из MetalDataManager.
        """
        manager = MetalDataManager() # Инициализирует менеджер данных для работы с API ЦБ.

        # 1. Проверяет доступность сервера ЦБ и наличие свежих данных.
        if not manager.update_rates():
            return "🥇🥈 <b>Металлы:</b> <i>Сервер ЦБ временно недоступен</i>"

        def format_row(code, name, icon):
            # 2. Извлекает список цен для конкретного металла [вчерашняя, сегодняшняя].
            prices = manager.metal_rates.get(code, [])

            # Если данных по металлу нет совсем, выводит заглушку.
            if not prices:
                return f"{icon} <b>{name}:</b> <i>нет данных</i>"

            # 3. Берет последнюю актуальную цену.
            curr = prices[-1]

            # 4. Если есть хотя бы две цены, рассчитывает динамику (рост/падение).
            if len(prices) > 1:
                prev = prices[-2]
                change = curr - prev
                pct = (change / prev) * 100

                # 5. Выбирает иконку тренда: стрелка вверх при росте, вниз при падении.
                arrow = "📈" if change >= 0 else "📉"
                # 6. Добавляет плюс перед положительным числом процента.
                sign = "+" if change > 0 else ""

                return f"{icon} <b>{name}:</b> {curr:,.2f} ₽ {arrow} ({sign}{pct:.2f}%)"

            # Если цена только одна, выводит её без динамики.
            return f"{icon} <b>{name}:</b> {curr:,.2f} ₽"

        # 7. Формирует строки для золота (код 1) и серебра (код 2)
        gold_row = format_row(1, "Золото", "🥇")
        silver_row = format_row(2, "Серебро", "🥈")

        # 8. Получает текущую дату для оформления заголовка.
        date_str = datetime.now().strftime('%d.%m.%Y')

        # Собирает все части в один итоговый текстовый блок для Telegram.
        return (
            f"✅ <b>Учетные цены металлов ЦБ РФ</b>\n"
            f"📅 на {date_str} (руб/грамм):\n\n"
            f"{gold_row}\n"
            f"{silver_row}\n\n"
            f"⚠️ <i>Динамика к предыдущему торговому дню.</i>"
        )
