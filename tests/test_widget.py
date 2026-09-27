import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "info, expected",
    [
        (
            "Visa 1234567812345678",
            "Visa 1234 56** **** 5678",
        ),
        (
            "MasterCard 1111222233334444",
            "MasterCard 1111 22** **** 4444",
        ),
        (
            "Счет 12345678901234567890",
            "Счет **7890",
        ),
    ],
)
def test_mask_account_card(info, expected):
    assert mask_account_card(info) == expected


@pytest.mark.parametrize(
    "date, expected",
    [
        (
            "2024-01-15T12:30:00",
            "15.01.2024",
        ),
        (
            "2023-12-31T23:59:59",
            "31.12.2023",
        ),
        (
            "2025-06-01T10:00:00",
            "01.06.2025",
        ),
    ],
)
def test_get_date(date, expected):
    assert get_date(date) == expected
