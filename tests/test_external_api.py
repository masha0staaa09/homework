from unittest.mock import Mock, patch

from src.external_api import convert_currency


def test_convert_currency_rub():
    transaction = {
        "operationAmount": {
            "amount": "1000.00",
            "currency": {
                "name": "руб.",
                "code": "RUB",
            },
        }
    }
    result = convert_currency(transaction)

    assert result == 1000.0


@patch("src.external_api.requests.get")
def test_convert_currency_usd(mock_get):
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "name": "USD",
                "code": "USD",
            },
        }
    }
    mock_response = Mock()
    mock_response.json.return_value = {"result": 8000.0}
    mock_get.return_value = mock_response

    result = convert_currency(transaction)

    assert result == 8000.0


@patch("src.external_api.requests.get")
def test_convert_currency_eur(mock_get):
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "name": "EUR",
                "code": "EUR",
            },
        }
    }
    mock_response = Mock()
    mock_response.json.return_value = {"result": 9000.0}
    mock_get.return_value = mock_response

    result = convert_currency(transaction)

    assert result == 9000.0
