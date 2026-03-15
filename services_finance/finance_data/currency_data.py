import logging
from config.settings import REQUIRED_CURRENCIES


def get_currency_report(manager):
    """
    Получает курсы валют, формирует отчет и возвращает отформатированную строку.
    """
    logger = logging.getLogger(__name__)

    # 1. Защита: Если данных нет совсем (пустой словарь в currency_rates) (если ЦБ не ответил).
    if not manager.currency_rates:
        logger.warning("Валюты отсутствуют в объекте manager!") # API молчит.
        return "💵 <b>Валюты:</b> <i>Ошибка банка или нет связи</i>"

    try:
        # 2. Защита: Проверка наличия нужных валют в словаре.
        # Проверка ключей в словаре manager.currency_rates.
        if not all(currency in manager.currency_rates for currency in REQUIRED_CURRENCIES):
            missing = [c for c in REQUIRED_CURRENCIES if c not in manager.currency_rates]
            logger.error(f"Неполная структура данных. Ожидались: {manager.currency_rates}, отсутствуют: {missing}")
            return "💵 <b>Валюты:</b> <i>Ошибка структуры данных ЦБ</i>"

        lines = []
        # 3. По очереди каждый код валюты из списка.
        for code in REQUIRED_CURRENCIES:
            # 4. Заходит в класс-менеджер и просит: «Все данные на валюту под кодом code».
            # На выходе получает словарь со всеми данными (цена, название, вчерашний курс).
            data = manager.get_currency_data(code)
            # 5. Вытаскивает номинал (обычно 1, но для CZK будет 10).
            nominal = data.get('Nominal', 1)
            # 6. Достает текущую цену. Если вдруг в данных пусто, берем 0.0.
            val = data.get('Value', 0.0) / nominal
            # 7. Достает вчерашнюю цену(Previous). Если вчерашней цены нет, подставляет сегодняшнюю(val).
            prev = data.get('Previous', val) / nominal
            # 8. Логическая проверка цены.
            icon = "📈" if val >= prev else "📉"
            # 9. Насколько изменился курс в рублях (разница между «сегодня» и «вчера»).
            diff = val - prev
            # 10. Добавляет в список.
            lines.append(f"<b>{code}:</b> {val:.2f} ₽ {icon} ({diff:+.2f})")

        header = "💵 <b>Курсы валют ЦБ РФ:</b>\n\n"
        return header + "\n".join(lines)

    except Exception as e:
        # .exception запишет traceback (строку ошибки).
        # Автоматически прикрепит к логу всю историю ошибки (какая именно строка упала).
        logger.exception(f"Критическая ошибка парсинга валют: {e}")
        return "💵 <b>Валюты:</b> <i>❌ Технический сбой</i>"
