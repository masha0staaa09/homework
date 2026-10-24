import json
import pandas as pd
from src.file_readers import read_report_csv_file
from datetime import datetime
from pathlib import Path
from src.external_api import get_currency_rates, get_stock_prices


def get_user_settings() -> dict:
    """Загружает настройки валют и акций."""
    settings_path = (
            Path(__file__).resolve().parent.parent / "user_settings.json"
    )
    with open(settings_path, encoding="utf-8") as file:
        return json.load(file)


def get_month_transactions(date_time: str) -> pd.DataFrame:
    """Возвращает операции с начала месяца по переданную дату."""
    current_date = datetime.strptime(
        date_time, "%Y-%m-%d %H:%M:%S"
    )
    transactions = read_report_csv_file("data/reports.csv")

    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"],
        format="%d.%m.%Y %H:%M:%S",
        errors="coerce",
    )

    start_date = current_date.replace(
        day=1, hour=0, minute=0, second=0
    )
    end_date = current_date.replace(
        hour=23, minute=59, second=59
    )

    return transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
    ].copy()


def get_cards(transactions: pd.DataFrame) -> list[dict]:
    """Возвращает расходы и кешбэк по каждой карте."""
    expenses = transactions.copy()
    expenses["Сумма платежа"] = pd.to_numeric(
        expenses["Сумма платежа"],
        errors="coerce",
    )

    expenses = expenses[
        expenses["Номер карты"].notna()
        & (expenses["Сумма платежа"] < 0)
    ].copy()

    result = []

    for card, group in expenses.groupby("Номер карты"):
        total_spent = float(round(-group["Сумма платежа"].sum(), 2))

        result.append({
            "last_digits": str(card)[-4:],
            "total_spent": total_spent,
            "cashback": float(round(total_spent / 100, 2)),
        })

    return result


def get_top_transactions(transactions: pd.DataFrame) -> list[dict]:
    """Возвращает пять транзакций с наибольшей суммой платежа."""
    data = transactions.copy()
    data["Сумма платежа"] = pd.to_numeric(
        data["Сумма платежа"],
        errors="coerce",
    )

    data = data.dropna(subset=["Сумма платежа"])

    top = data.nlargest(5, "Сумма платежа")

    result = []

    for _, transaction in top.iterrows():
        result.append({
            "date": transaction["Дата операции"].strftime("%d.%m.%Y"),
            "amount": float(transaction["Сумма платежа"]),
            "category": str(transaction["Категория"]),
            "description": str(transaction["Описание"]),
        })

    return result


def get_greeting(date_time: str) -> str:
    """Возвращает приветствие в зависимости от времени."""
    current_time = datetime.strptime(
        date_time, "%Y-%m-%d %H:%M:%S"
    )
    hour = current_time.hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_main_page_data(date_time: str) -> str:
    """Формирует JSON-ответ для главной страницы."""
    settings = get_user_settings()
    transactions = get_month_transactions(date_time)
    result = {
        "greeting": get_greeting(date_time),
        "cards": get_cards(transactions),
        "top_transactions": get_top_transactions(transactions),
        "currency_rates": get_currency_rates(
            settings["user_currencies"]
        ),
        "stock_prices": get_stock_prices(
            settings["user_stocks"]
        ),
    }

    return json.dumps(result, ensure_ascii=False, indent=4)
