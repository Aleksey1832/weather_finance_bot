import logging
import yfinance as yf
from utils.cache_manager import finance_cache


class OilDataManager:
    """
    Менеджер поставки данных цен на нефть.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cache = finance_cache
        # BZ=F — тикер фьючерса на нефть Brent на Yahoo.
        self.oil_ticker = yf.Ticker("BZ=F")
        self.data = None

    def fetch_oil_price(self):
        """
        Получение цены на нефть Brent.
        """
        # 1. Проверяем общий кэш
        cached_val = self.cache.get("brent_oil")
        if cached_val is not None:
            self.logger.info("📦 Нефть взята из кэша")
            return cached_val
        try:
            # 2. Если в кэше нет — идем в API.
            # Получает историю за 7 дней.
            df = self.oil_ticker.history(period="5d", interval="1m")

            if df is not None and not df.empty:
                self.cache.set("brent_oil", df)
                self.data = df
                self.logger.info("✅ Данные по нефти успешно получены из API")
                self.logger.debug(f"Получено строк: {len(df)}")
                return df
            return None

        except Exception as e:
            self.logger.error(f"Ошибка при загрузке нефти: {e}")
            self.data = None  # Сбрасывает, чтобы не использовать мусор.
            return None
