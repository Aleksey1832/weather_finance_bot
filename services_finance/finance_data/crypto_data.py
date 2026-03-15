import logging
from config.settings import REQUIRED_CRYPTS, ICONS


def get_crypto_report(manager, usd_rate: float):
    """
        Получает курсы крипты, формирует отчет и возвращает отформатированную строку.
    """
    logger = logging.getLogger(__name__)

    # 1. Защита: Если данных нет совсем (пустой словарь в rates) (если CoinGecko не ответил).
    if not manager.crypto_rates:
        logger.warning("Крипто-данные отсутствуют в объекте manager!") # API молчит.
        return "₿ <b>Крипто:</b> <i>Данные временно недоступны</i>"

    try:
        # 2. Защита: Проверка структуры (CoinGecko использует полные ID).
        # Проверка ключей в словаре manager.crypto_rates.
        if not all(coin in manager.crypto_rates for coin in REQUIRED_CRYPTS):
            missing = [c for c in REQUIRED_CRYPTS if c not in manager.crypto_rates]
            logger.error(f"Неполная структура данных. Ожидались: {manager.crypto_rates}, отсутствуют: {missing}")
            return "₿ <b>Крипто:</b> <i>Ошибка структуры данных API</i>"

        # 3. Словарь иконок.
        icons = ICONS

        lines = []
        for coin_id in REQUIRED_CRYPTS:
            # 4. Цену в USD через метод get_price.
            price_usd = manager.get_price(coin_id)

            # 5. Проверка, что данные от CoinGecko не биты.
            if coin_id == 'bitcoin' and price_usd == 0:
                logger.error("Критический сбой: BTC = 0")
                return "₿ <b>Крипто:</b> <i>Ошибка котировок</i>"

            # 6. Сокращенное имя для красоты (Bitcoin -> BTC).
            symbol = coin_id[:3].upper() if coin_id != 'dogecoin' else 'DOGE'
            if coin_id == 'bitcoin': symbol = 'BTC'
            if coin_id == 'ethereum': symbol = 'ETH'
            icon = icons.get(coin_id, '🪙')

            # 7. f-строка с вложенным форматированием через временную переменную.
            formatted_usd = f"{price_usd:,.0f}" if price_usd > 100 else f"{price_usd:,.2f}"

            # 8. Подсчет в рублях, если есть курс.
            rub_text = ""
            if isinstance(usd_rate, (int, float)) and usd_rate > 0:
                price_rub = price_usd * usd_rate
                # Для дорогих монет убираем копейки, для дешевых оставляем.
                formatted_rub = f"{price_rub:,.0f}" if price_rub > 100 else f"{price_rub:,.2f}"
                rub_text = f" / {formatted_rub} ₽"
            else:
                # Логируем только один раз, чтобы не спамить в цикле.
                if coin_id == REQUIRED_CRYPTS[0]:
                    logger.warning(f"Нет расчета в руб. Некорректный usd_rate: {usd_rate}")

            # 9. Динамическая иконка тренда (сравнение с 24ч изменением из данных API).
            # CoinGecko обычно отдает это в поле 'usd_24h_change'.
            change_pct = manager.crypto_rates.get(coin_id, {}).get('usd_24h_change', 0)
            trend = "📈" if change_pct >= 0 else "📉"

            # 10. Составляет список report.
            lines.append(f"{icon} <b>{symbol}:</b> ${formatted_usd}{rub_text} {trend}")

        logger.info("Крипто-отчет успешно сформирован динамически")

        header = "✅ <b>Курсы криптовалют:</b>\n\n"
        return header + "\n".join(lines)

    except Exception as e:
        # .exception запишет traceback (строку ошибки).
        # Автоматически прикрепит к логу всю историю ошибки (какая именно строка упала).
        logger.exception(f"Критическая ошибка парсинга крипты: {e}")
        return "₿ <b>Крипто:</b> <i>❌ Технический сбой</i>"
