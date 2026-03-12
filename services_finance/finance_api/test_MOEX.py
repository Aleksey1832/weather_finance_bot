import requests
import json


# !!! ВАЖНО: Укажи АКТУАЛЬНЫЙ тикер фьючерса на Brent с сайта MOEX !!!
# Например, если тикер BR-6.24, то используй "BR-6.24"BRJ6
ACTUAL_BRENT_TICKER = "BRN4"  # ЗАМЕНИ НА АКТУАЛЬНЫЙ!

def get_brent_futures_price(ticker: str):


    # URL для получения рыночных данных (последняя сделка, bid, offer)
    url = f"http://iss.moex.com/iss/engines/futures/markets/forts/securities/{ticker}.json?iss.only=marketdata&marketdata.columns=LAST,BID,OFFER"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Вызовет исключение для плохих ответов (4xx или 5xx)

        data = response.json()

        # Парсим данные. Структура JSON может немного отличаться,
        # поэтому важно посмотреть полный ответ или использовать библиотеки.
        # Этот пример парсинга может потребовать корректировки.

        marketdata = data.get("marketdata", {}).get("data")

        if marketdata and len(marketdata) > 0:
            # Предполагаем, что первая строка данных содержит нужную информацию
            # Индексы столбцов нужно будет уточнить по полному ответу API
            # LAST - 1, BID - 2, OFFER - 3 (это примерные индексы, МОЖЕТ БЫТЬ НЕВЕРНО)
            # Лучше всего просмотреть структуру data["marketdata"]["columns"]

            columns = data["marketdata"]["columns"]

            try:
                last_index = columns.index("LAST")
                bid_index = columns.index("BID")
                offer_index = columns.index("OFFER")
            except ValueError as e:
                print(f"Ошибка: Не удалось найти нужные столбцы в ответе API. {e}")
                print("Доступные столбцы:", columns)
                exit()

            current_price_data = marketdata[0]  # Берем первую строку данных

            last_price = current_price_data[last_index]
            bid_price = current_price_data[bid_index]
            offer_price = current_price_data[offer_index]

            print(f"Актуальная цена на нефть Brent (Тикер: {ACTUAL_BRENT_TICKER}):")
            print(f"  Последняя сделка (LAST): {last_price}")
            print(f"  Лучшая цена покупки (BID): {bid_price}")
            print(f"  Лучшая цена продажи (OFFER): {offer_price}")
        else:
            print(f"Не удалось получить рыночные данные для тикера {ACTUAL_BRENT_TICKER}.")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса к API MOEX: {e}")
    except json.JSONDecodeError:
        print("Ошибка: Не удалось декодировать JSON-ответ от API MOEX.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    print("--- Тестирование получения данных о Brent ---")
    # Здесь мы вызываем функцию, но это происходит только если этот файл запускается НАПРЯМУЮ,
    # а не импортируется в другой файл.
    # Это как "запустить только этот инструмент, не дом целиком".
    brent_data = get_brent_futures_price(ACTUAL_BRENT_TICKER)

    if brent_data:
        print(f"Получены данные:")
        print(f"  Тикер: {brent_data['ticker']}")
        print(f"  Последняя: {brent_data['last_price']}")
        print(f"  BID: {brent_data['bid_price']}")
        print(f"  OFFER: {brent_data['offer_price']}")
    else:
        print("Не удалось получить данные о Brent.")
    print("--- Тестирование завершено ---")