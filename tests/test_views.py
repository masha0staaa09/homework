import json
import pytest
import pandas as pd
from src.views import (
    get_greeting,
    get_month_transactions,
    get_cards,
    get_top_transactions,
    get_user_settings,
    get_main_page_data,
)


@pytest.mark.parametrize(
    "date_time, expected",
    [
        ("2021-12-21 05:59:00", "Доброй ночи"),
        ("2021-12-21 06:00:00", "Доброе утро"),
        ("2021-12-21 11:59:00", "Доброе утро"),
        ("2021-12-21 12:00:00", "Добрый день"),
        ("2021-12-21 17:59:00", "Добрый день"),
        ("2021-12-21 18:00:00", "Добрый вечер"),
        ("2021-12-21 22:59:00", "Добрый вечер"),
        ("2021-12-21 23:00:00", "Доброй ночи"),
    ],
)
def test_get_greeting(date_time, expected):
    assert get_greeting(date_time) == expected


def test_get_month_transactions(monkeypatch):
    transactions = pd.DataFrame(
        {
            "Дата операции": [
                "31.12.2021 12:00:00",
                "01.12.2021 00:00:00",
                "21.12.2021 14:00:00",
                "01.11.2021 12:00:00",
            ],
            "Сумма платежа": [-100, -200, -300, -400],
        }
    )
    monkeypatch.setattr(
        "src.views.read_report_csv_file",
        lambda _: transactions.copy(),
    )

    result = get_month_transactions("2021-12-21 14:30:00")

    assert len(result) == 2
    assert result["Сумма платежа"].tolist() == [-200, -300]


def test_get_cards():
    transactions = pd.DataFrame(
        {
            "Номер карты": ["*1234", "*1234", "*5678", "*5678"],
            "Сумма платежа": [-1000, -500, -200, 300],
        }
    )
    result = get_cards(transactions)

    assert result == [
        {
            "last_digits": "1234",
            "total_spent": 1500.0,
            "cashback": 15.0,
        },
        {
            "last_digits": "5678",
            "total_spent": 200.0,
            "cashback": 2.0,
        },
    ]


def test_get_top_transactions():
    transactions = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(
                [
                    "2021-12-01 12:00:00", "2021-12-02 12:00:00",
                    "2021-12-03 12:00:00", "2021-12-04 12:00:00",
                    "2021-12-05 12:00:00", "2021-12-06 12:00:00",
                ]
            ),
            "Сумма платежа": [-100, 500, 300, 200, 100, 50],
            "Категория": [
                "Еда", "Техника", "Дом", "Транспорт", "Аптеки", "Кафе"],
            "Описание": [
                "Покупка 1",
                "Покупка 2",
                "Покупка 3",
                "Покупка 4",
                "Покупка 5",
                "Покупка 6"
            ],
        }
    )
    result = get_top_transactions(transactions)

    assert len(result) == 5
    assert result[0]["amount"] == 500.0
    assert result[0]["category"] == "Техника"
    assert result[0]["description"] == "Покупка 2"
    assert all(isinstance(item["amount"], float) for item in result)

    # Проверяем сортировку по убыванию суммы
    amounts = [item["amount"] for item in result]
    assert amounts == sorted(amounts, reverse=True)

    # Проверяем обязательные поля и формат даты
    for item in result:
        assert set(item.keys()) >= {
            "date", "amount", "category", "description"
        }
        assert len(item["date"]) == 10
        assert item["date"][2] == "."
        assert item["date"][5] == "."


def test_get_user_settings(tmp_path, monkeypatch):
    settings_file = tmp_path / "user_settings.json"
    settings_file.write_text(
        '{"user_currencies": ["USD", "EUR"], '
        '"user_stocks": ["AAPL", "AMZN"]}',
        encoding="utf-8",
    )
    fake_views_path = tmp_path / "src" / "views.py"
    fake_views_path.parent.mkdir()

    monkeypatch.setattr(
        "src.views.__file__",
        str(fake_views_path),
    )

    result = get_user_settings()

    assert result == {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN"],
    }


def test_get_main_page_data(monkeypatch):
    monkeypatch.setattr(
        "src.views.get_user_settings",
        lambda: {"user_currencies": ["USD"], "user_stocks": ["AAPL"], },
    )
    monkeypatch.setattr(
        "src.views.get_month_transactions",
        lambda _: pd.DataFrame(
            columns=[
                "Дата операции",
                "Номер карты",
                "Сумма платежа",
                "Категория",
                "Описание",
            ]
        ),
    )
    monkeypatch.setattr(
        "src.views.get_currency_rates",
        lambda currencies:
        [{"currency": "USD", "rate": 90.0}],
    )
    monkeypatch.setattr(
        "src.views.get_stock_prices",
        lambda stocks:
        [{"stock": "AAPL", "price": 200.0}],
    )
    result = json.loads(
        get_main_page_data("2021-12-21 14:30:00")
    )

    assert result["greeting"] == "Добрый день"
    assert result["cards"] == []
    assert result["top_transactions"] == []
    assert result["currency_rates"] == [
        {"currency": "USD", "rate": 90.0}
    ]
    assert result["stock_prices"] == [
        {"stock": "AAPL", "price": 200.0}
    ]


def test_get_main_page_data_with_card(monkeypatch):
    monkeypatch.setattr(
        "src.views.get_user_settings",
        lambda:
        {"user_currencies": [],
         "user_stocks": []},
    )
    monkeypatch.setattr(
        "src.views.get_month_transactions",
        lambda _:
        pd.DataFrame({
            "Дата операции": pd.to_datetime(["2021-12-01 12:00:00"]),
            "Номер карты": ["*1234"], "Сумма платежа": [-1000],
            "Категория": ["Еда"],
            "Описание": ["Покупка"],
        }),
    )
    monkeypatch.setattr(
        "src.views.get_currency_rates",
        lambda currencies: [],
    )
    monkeypatch.setattr(
        "src.views.get_stock_prices",
        lambda stocks: [],
    )
    result = json.loads(
        get_main_page_data("2021-12-21 14:30:00")
    )

    assert len(result["cards"]) >= 1
    assert result["cards"][0]["last_digits"] == "1234"
