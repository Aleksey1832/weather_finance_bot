import datetime
import pandas as pd


class MetalFormatter:
    """
    Универсальный форматировщик для металлов.
    """

    # Словарь настроек: ключ — тикер, значение — (Иконка, Название)
    CONFIG = {
        "GC=F": ("🥇", "Gold"),
        "SI=F": ("🥈", "Silver")
    }

    @staticmethod
    def _format_row(table, icon, name, usd_rate: float):
        """Внутренний метод для подготовки одной строки (Золото или Серебро)."""
        if table is None or table.empty:
            return f"{icon} <b>{name}:</b> <i>данные недоступны</i>"

        try:
            last_row = table.iloc[-1]
            if pd.isna(last_row['Close']) or pd.isna(last_row['Open']):
                return f"{icon} <b>{name}:</b> <i>обновление...</i>"

            last_price = float(last_row['Close'])
            open_price = float(last_row['Open'])

            # Динамика и иконка.
            change_icon = "📈" if last_price >= open_price else "📉"
            change_pct = ((last_price - open_price) / open_price) * 100

            # Форматирует доллары (Золото с запятыми, Серебро обычно).
            price_fmt = f"{last_price:,.2f}" if "Gold" in name else f"{last_price:.2f}"

            # Подсчет в рублях, если есть курс.
            rub_text = ""
            if isinstance(usd_rate, (int, float)) and usd_rate > 0:
                price_rub = last_price * usd_rate
                # Для золота (оно дороже 100 руб) убираем копейки, для серебра оставляем
                formatted_rub = f"{price_rub:,.0f}" if price_rub > 100 else f"{price_rub:,.2f}"
                rub_text = f" / {formatted_rub} ₽"

            return f"{icon} <b>${price_fmt}</b>{rub_text} {change_icon} ({change_pct:+.2f}%)"
        except:
            return f"{icon} <b>{name}:</b> <i>ошибка</i>"

    @staticmethod
    def get_metals_report(gold_table, silver_table, usd_rate: float):
        """Собирает общий отчет с единым заголовком и проверкой даты."""

        # 1. Определяем дату (берем по золоту, они в одной связке)
        if gold_table is not None and not gold_table.empty:
            last_dt = gold_table.index[-1]
        elif silver_table is not None and not silver_table.empty:
            last_dt = silver_table.index[-1]
        else:
            return "🥇🥈 <b>Металлы:</b> <i>Биржа закрыта</i>"

        # 2. Логика заголовка (Label)
        today = datetime.date.today()
        date_str = last_dt.strftime('%H:%M, %d.%m.%Y')

        if last_dt.date() == today:
            label = "<b>Актуальные тикеры металлов (унц.):</b>"
        else:
            label = f"Последняя цена металлов (унц.) {date_str}\n⚠️ <i>Торги приостановлены (выходной)</i>"

        # 3. Получаем отформатированные строки
        gold_row = MetalFormatter._format_row(gold_table, "🥇", "Gold", usd_rate)
        silver_row = MetalFormatter._format_row(silver_table, "🥈", "Silver", usd_rate)

        # 4. Сборка итогового блока
        status_header = "<b>Котировки фьючерсов металлов</b>"

        return (
            f"✅ {status_header}\n"
            f"{label}\n\n"
            f"{gold_row}\n"
            f"{silver_row}"
        )
