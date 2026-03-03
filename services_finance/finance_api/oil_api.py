import logging
import yfinance as yf


class OilDataManager:
    """
    Менеджер поставки данных цен на нефть.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # BZ=F — тикер фьючерса на нефть Brent на Yahoo.
        self.oil_ticker = yf.Ticker("BZ=F")
        self.data = None

    def fetch_oil_price(self):
        """
        Получение цены на нефть Brent.
        """
        try:
            # Получает историю за 7 дней.
            df = self.oil_ticker.history(period="5d", interval="1m")

            if df is not None and not df.empty:
                self.data = df
                self.logger.info("✅ Данные по нефти успешно получены: ")
                self.logger.debug(f"Получено строк: {len(df)}")
                return df
            return None

        except Exception as e:
            self.logger.error(f"Ошибка при загрузке нефти: {e}")
            self.data = None  # Сбрасывает, чтобы не использовать мусор.
            return None
