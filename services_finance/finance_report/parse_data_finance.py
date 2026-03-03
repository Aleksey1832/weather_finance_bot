from services_finance.finance_api.currency_api import CurrencyDataManager
from services_finance.finance_api.crypto_api import CryptoDataManager
from services_finance.finance_api.oil_api import OilDataManager
from services_finance.finance_api.metal_api import MetalDataManager
from services_finance.finance_data.metal_data import MetalFormatter
from services_finance.finance_data.currency_data import get_currency_report
from services_finance.finance_data.crypto_data import get_crypto_report
from services_finance.finance_data.oil_data import get_oil_price


def get_full_finance_report():
    """
    Формирование отчета.
    """
    # 1. Создание финансов.
    # 1.1 Создание валютчика и обновление.
    currency_manager = CurrencyDataManager()
    currency_manager.update_rates()  # Это единственный запрос к ЦБ!

    # 1.2 Создание крипты и обновление.
    crypto_manager = CryptoDataManager()
    crypto_manager.update_rates()  # Это единственный запрос к CoinGecko!

    # 1.3 Создание запроса на нефть.
    manager = OilDataManager()
    oil_table = manager.fetch_oil_price()

    # 1.4 Создание запроса на металлы.
    metal_manager = MetalDataManager()
    gold_t, silver_t = metal_manager.fetch_metals()

    # 2. Курс usd для крипты.
    usd_value = currency_manager.get_usd_value()

    # 3. Раздача данных функциям.
    # 3.1 Передача всего объекта в отчет по валютам.
    currency = get_currency_report(currency_manager)

    # 3.2 Передача всего объекта и числа (курс usd) в отчет по крипте.
    crypto = get_crypto_report(crypto_manager, usd_value)

    # 3.3 Передача всего объекта в отчет по нефти.
    oil = get_oil_price(oil_table)

    # 3.4 Передача всего объекта в отчет по металлам.
    metals = MetalFormatter.get_metals_report(gold_t, silver_t, usd_value)

    return (
        "<b>📊 ФИНАНСОВЫЙ ОТЧЕТ</b>\n"
        "━━━━━━━━━━━━━━━\n"
        f"{currency}\n"
        "━━━━━━━━━━━━━━━\n"
        f"{crypto}\n"
        "━━━━━━━━━━━━━━━\n"
        f"{oil}\n"
        "━━━━━━━━━━━━━━━\n"
        f"{metals}\n"
        "━━━━━━━━━━━━━━━\n"
        "✨ <b>Удачных инвестиций!</b> ✨"
    )
