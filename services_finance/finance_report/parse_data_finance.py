from services_finance.finance_api.currency_api import CurrencyDataManager
from services_finance.finance_api.crypto_api import CryptoDataManager
from services_finance.finance_api.oil_api import OilDataManager
from services_finance.finance_api.metal_api import MetalDataManager
from services_finance.finance_data.metal_data import MetalFormatter
from services_finance.finance_data.currency_data import get_currency_report
from services_finance.finance_data.crypto_data import get_crypto_report
from services_finance.finance_data.oil_data import OilFormatter


def get_full_finance_report():
    """
    Формирование отчета.
    """
    # --- Создание финансов ---
    # 1 Создание валютчика и обновление.
    currency_manager = CurrencyDataManager()
    currency_manager.update_rates()  # Это единственный запрос к ЦБ!

    # 2 Создание крипты и обновление.
    crypto_manager = CryptoDataManager()
    crypto_manager.update_rates()  # Это единственный запрос к CoinGecko!

    # 3. Загрузка данных по металлам и обновление.
    metal_manager = MetalDataManager()
    metal_manager.update_rates()

    # 4. Загрузка данных по нефти.
    manager = OilDataManager()
    oil_table = manager.fetch_oil_price()

    # --- СБОРКА ТЕКСТОВЫХ БЛОКОВ ---
    # 5. Курс usd для крипты.
    usd_value = currency_manager.get_usd_value()

    # Раздача данных функциям.
    # 6. Валютный отчет. Передача всего объекта в отчет по валютам.
    currency = get_currency_report(currency_manager)

    # 7. Крипто отчет. Передача всего объекта и числа (курс usd) в отчет по крипте.
    crypto = get_crypto_report(crypto_manager, usd_value)

    # 9. Металлы. Форматтер сам разберется с ЦБ РФ внутри.
    metals = MetalFormatter.get_metals_report(metal_manager)

    # 8. Нефтяной отчет. Функция сама создаст менеджера внутри и сходит на Yahoo.
    oil = OilFormatter.get_oil_report(oil_table)

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
