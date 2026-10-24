import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


def convert_currency(transaction: dict) -> float:
    """Конвертирует сумму транзакции в рубли."""
    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]
    if currency == "RUB":
        return amount

    url = "https://api.apilayer.com/exchangerates_data/convert"

    if API_KEY is None:
        raise ValueError("API_KEY не найден в переменных окружения")

    headers = {
        "apikey": API_KEY,
    }

    params = {
        "from": currency,
        "to": "RUB",
        "amount": amount,
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()

    return float(data["result"])


def get_currency_rates(currencies: list[str]) -> list[dict]:
    """Возвращает текущие курсы указанных валют к рублю."""
    result = []
    for currency in currencies:
        if currency == "RUB":
            result.append({
                "currency": currency,
                "rate": 1.0,
            })
            continue

        url = f"https://api.frankfurter.dev/v2/rate/{currency}/RUB"

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            rate = float(data["rate"])

            if rate <= 0:
                continue

            result.append({
                "currency": currency,
                "rate": rate,
            })

        except (requests.RequestException, ValueError, KeyError, TypeError):
            continue

    return result


def get_stock_prices(stocks: list[str]) -> list[dict]:
    """Возвращает последние доступные цены акций."""
    result = []
    for stock in stocks:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock}"
        params = {
            "range": "1d",
            "interval": "1d",
        }
        headers = {
            "User-Agent": "Mozilla/5.0",
        }

        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()

            stock_data = data["chart"]["result"][0]
            price = float(stock_data["meta"]["regularMarketPrice"])

            if price <= 0:
                continue

            result.append({
                "stock": stock,
                "price": price,
            })

        except (
            requests.RequestException,
            ValueError,
            KeyError,
            TypeError,
            IndexError,
        ):
            continue

    return result
