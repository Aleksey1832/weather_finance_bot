from datetime import datetime
import pandas as pd


class OilFormatter:
    """
    Получает отчет по нефти, формирует отчет и возвращает отформатированную строку.
    """

    @staticmethod
    def get_oil_report(oil_table):

        # 1. Защита: Если данных нет совсем.
        if oil_table is None or oil_table.empty:
            return "🛢 <b>Нефть Brent:</b> <i>Биржа закрыта или нет связи</i>"

        try:
            # 2. Защита: Проверка наличие колонок (чтобы не вылететь по KeyError).
            if 'Close' not in oil_table.columns or 'Open' not in oil_table.columns:
                return "🛢 <b>Нефть:</b> <i>Ошибка структуры данных</i>"

            # 3. Достает последние строку и её дату (значения из таблицы).
            last_row = oil_table.iloc[-1]

            # 4. Если в последней строке вместо цифры - пусто NaN (Not a Number).
            if pd.isna(last_row['Close']) or pd.isna(last_row['Open']):
                return "🛢 <b>Нефть:</b> <i>Данные обновляются...</i>"

            # 5. oil_table.index[-1] — это время закрытия торгов в формате Timestamp.
            last_dt = oil_table.index[-1]

            last_price = float(last_row['Close'])
            open_price = float(last_row['Open'])

            # 6. Сравнение даты для заголовка.
            today = datetime.now().date()
            is_today = last_dt.date() == today

            # 7. Форматирует дату для вывода.
            date_str = last_dt.strftime('%H:%M, %d.%m.%Y')

            # 8. Если сегодня выходной, добавляет дату.
            if is_today:
                label = "Актуальный тикер нефти Brent:\n\n"
            else:
                label = f"Последняя цена Brent {date_str}:\n⚠️ <i>Торги приостановлены (выходной)</i>\n"

            status = "<b>Котировки фьючерса нефти</b>\n"
            icon = "📈" if last_price >= open_price else "📉"
            change_pct = ((last_price - open_price) / open_price) * 100

            return f"✅ <b>{status}{label}</b> 🛢${last_price:.2f} {icon} ({change_pct:+.2f}%)"

        except Exception as e:
            print(f"Ошибка парсинга нефти: {e}")
            return "🛢 <b>Нефть:</b> <i>❌ Технический сбой</i>"
