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


@patch("src.external_api.requests.get")
def test_get_currency_rates_api_error(mock_get):
    from src.external_api import get_currency_rates
    import requests
    mock_get.side_effect = requests.ConnectionError("API error")

    result = get_currency_rates(["USD", "RUB"])

    assert result == [{"currency": "RUB", "rate": 1.0}]


@patch("src.external_api.requests.get")
def test_get_stock_prices_api_error(mock_get):
    from src.external_api import get_stock_prices
    import requests
    mock_get.side_effect = requests.ConnectionError("API error")

    result = get_stock_prices(["AAPL"])

    assert result == []


@patch("src.external_api.requests.get")
def test_get_stock_prices_empty_result(mock_get):
    from src.external_api import get_stock_prices
    mock_response = Mock()
    mock_response.json.return_value = {
        "chart": {
            "result": None,
            "error": None,
        }
    }
    mock_get.return_value = mock_response

    result = get_stock_prices(["AAPL"])

    assert result == []


@patch("src.external_api.requests.get")
def test_get_currency_rates_missing_rate(mock_get):
    from src.external_api import get_currency_rates
    mock_response = Mock()
    mock_response.json.return_value = {"unexpected": "data"}
    mock_get.return_value = mock_response

    result = get_currency_rates(["USD"])

    assert result == []


@patch("src.external_api.requests.get")
def test_get_currency_rates_success(mock_get):
    from src.external_api import get_currency_rates
    mock_response = Mock()
    mock_response.json.return_value = {"rate": 92.5}
    mock_get.return_value = mock_response

    result = get_currency_rates(["USD"])

    assert result == [{"currency": "USD", "rate": 92.5}]
    assert isinstance(result[0]["rate"], float)
    assert result[0]["rate"] > 0
    assert set(result[0].keys()) == {"currency", "rate"}


@patch("src.external_api.requests.get")
def test_get_currency_rates_multiple_currencies(mock_get):
    from src.external_api import get_currency_rates
    mock_response = Mock()
    mock_response.json.side_effect = [
        {"rate": 92.5},
        {"rate": 99.0},
    ]
    mock_get.return_value = mock_response

    result = get_currency_rates(["USD", "EUR", "RUB"])

    assert result == [
        {"currency": "USD", "rate": 92.5},
        {"currency": "EUR", "rate": 99.0},
        {"currency": "RUB", "rate": 1.0},
    ]


@patch("src.external_api.requests.get")
def test_get_stock_prices_success(mock_get):
    from src.external_api import get_stock_prices
    mock_response = Mock()
    mock_response.json.return_value = {
        "chart": {
            "result": [
                {
                    "meta": {
                        "regularMarketPrice": 200.5,
                    }
                }
            ],
            "error": None,
        }
    }
    mock_get.return_value = mock_response

    result = get_stock_prices(["AAPL"])

    assert result == [{"stock": "AAPL", "price": 200.5}]
    assert isinstance(result[0]["stock"], str)
    assert isinstance(result[0]["price"], float)
    assert result[0]["price"] > 0


@patch("src.external_api.requests.get")
def test_get_stock_prices_multiple_stocks(mock_get):
    from src.external_api import get_stock_prices
    mock_response_aapl = Mock()
    mock_response_aapl.json.return_value = {
        "chart": {
            "result": [{"meta": {"regularMarketPrice": 200.5}}],
            "error": None,
        }
    }

    mock_response_msft = Mock()
    mock_response_msft.json.return_value = {
        "chart": {
            "result": [{"meta": {"regularMarketPrice": 400.0}}],
            "error": None,
        }
    }

    mock_get.side_effect = [
        mock_response_aapl,
        mock_response_msft,
    ]

    result = get_stock_prices(["AAPL", "MSFT"])

    assert result == [
        {"stock": "AAPL", "price": 200.5},
        {"stock": "MSFT", "price": 400.0},
    ]


@patch("src.external_api.requests.get")
def test_get_currency_rates_continues_after_error(mock_get):
    import requests
    failed_response = Mock()
    failed_response.raise_for_status.side_effect = (
        requests.HTTPError("Server error")
    )

    successful_response = Mock()
    successful_response.raise_for_status.return_value = None
    successful_response.json.return_value = {"rate": 95.0}

    mock_get.side_effect = [
        failed_response,
        successful_response,
    ]

    from src.external_api import get_currency_rates

    result = get_currency_rates(["USD", "EUR"])

    assert result == [{"currency": "EUR", "rate": 95.0}]


@patch("src.external_api.requests.get")
def test_get_stock_prices_continues_after_error(mock_get):
    import requests
    failed_response = Mock()
    failed_response.raise_for_status.side_effect = (
        requests.HTTPError("Server error")
    )

    successful_response = Mock()
    successful_response.raise_for_status.return_value = None
    successful_response.json.return_value = {
        "chart": {
            "result": [
                {"meta": {"regularMarketPrice": 400.0}}
            ],
            "error": None,
        }
    }

    mock_get.side_effect = [
        failed_response,
        successful_response,
    ]

    from src.external_api import get_stock_prices

    result = get_stock_prices(["AAPL", "MSFT"])

    assert result == [{"stock": "MSFT", "price": 400.0}]
