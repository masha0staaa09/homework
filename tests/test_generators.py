import pytest

from src.generators import (card_number_generator, filter_by_currency,
                            transaction_descriptions)


@pytest.fixture
def transactions():
    return [
        {
            "id": 1,
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации"
        },
        {
            "id": 2,
            "operationAmount": {
                "amount": "200.00",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет"
        },
        {
            "id": 3,
            "operationAmount": {
                "amount": "300.00",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту"
        },
    ]

@pytest.mark.parametrize(
    "currency, expected_ids",
    [
        ("USD", [1, 3]),
        ("RUB", [2]),
        ("EUR", []),
    ],
)
def test_filter_by_currency(transactions,
                            currency,
                            expected_ids):
    result = list(filter_by_currency(transactions, currency))
    assert [transaction["id"] for transaction in result] == expected_ids


def test_transaction_descriptions(transactions):
    result = list(transaction_descriptions(transactions))
    assert result == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
    ]


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (1, 3, [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
        ]),
        (9999999999999998, 9999999999999999, [
            "9999 9999 9999 9998",
            "9999 9999 9999 9999",
        ]),
    ],
)
def test_card_number_generator(start, stop, expected):
    result = list(card_number_generator(start, stop))
    assert result == expected


def test_filter_by_currency_empty():
    result = list(filter_by_currency([], "USD"))
    assert result == []


def test_transaction_descriptions_empty():
    result = list(transaction_descriptions([]))
    assert result == []


def test_card_number_generator_stop():
    generator = card_number_generator(1, 2)
    assert next(generator) == "0000 0000 0000 0001"
    assert next(generator) == "0000 0000 0000 0002"

    with pytest.raises(StopIteration):
        next(generator)