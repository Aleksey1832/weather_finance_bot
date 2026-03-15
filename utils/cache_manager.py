import time

class FinanceCache:
    """
    Создание единого механизма кэширования.
    """
    def __init__(self, ttl_seconds=300):
        self.ttl = ttl_seconds
        self._data = {}  # Хранит данные по ключам: 'oil', 'btc', 'usd'.
        self._expiry = {} # Хранит время истечения для каждого ключа.

    def get(self, key):
        """Получить данные, если они еще свежие."""
        now = time.time()
        if key in self._data and now < self._expiry[key]:
            return self._data[key]
        return None

    def set(self, key, value):
        """Сохранить данные и установить время истечения."""
        self._data[key] = value
        self._expiry[key] = time.time() + self.ttl

# Создаем один экземпляр на весь проект
finance_cache = FinanceCache(ttl_seconds=300)
