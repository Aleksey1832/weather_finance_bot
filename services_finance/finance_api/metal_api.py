import logging
import yfinance as yf


class MetalDataManager:
    def __init__(self):
        # Тикеры для золота и серебра
        self.logger = logging.getLogger(__name__)
        self.gold_ticker = yf.Ticker("GC=F")
        self.silver_ticker = yf.Ticker("SI=F")

    def fetch_metals(self):
        """Загружает данные по обоим металлам за один вызов."""
        # Запрашивает данные (как и с нефтью, берем с запасом на выходные).
        try:
            # 5 дней, чтобы гарантированно перекрыть выходные.
            gold_data = self.gold_ticker.history(period="5d", interval="1h")
            silver_data = self.silver_ticker.history(period="5d", interval="1h")

            self.logger.info("🥇🥈 Данные по драгметаллам успешно обновлены")
            return gold_data, silver_data

        except Exception as e:
            self.logger.error(f"❌ Ошибка при загрузке металлов: {e}")
            return None, None
