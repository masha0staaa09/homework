import pytest
from _pytest import fixtures

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def transactions():
    return [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
    ]


@pytest.mark.parametrize(
    "data, state, expected",
    [
        (
                [
                    {"id": 1, "state": "EXECUTED"},
                    {"id": 2, "state": "CANCELED"},
                    {"id": 3, "state": "EXECUTED"},
                ], "EXECUTED",
                [
                    {"id": 1, "state": "EXECUTED"},
                    {"id": 3, "state": "EXECUTED"},
                ],
        ),
        (
                [
                    {"id": 1, "state": "EXECUTED"},
                    {"id": 2, "state": "CANCELED"},
                ],
                "CANCELED",
                [
                    {"id": 2, "state": "CANCELED"},
                ],
        ),
        (
                [
                    {"id": 1, "state": "EXECUTED"},
                    {"id": 2, "state": "CANCELED"},
                ],
                "PENDING",
                [],
        ),
    ],
)
def test_filter_by_state(data, state, expected):
    assert filter_by_state(data, state) == expected


def test_filter_by_state_default(transactions):
    expected = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 3, "state": "EXECUTED"},
    ]

    assert filter_by_state(transactions) == expected


@pytest.mark.parametrize(
    "data, descending, expected",
    [
        (
                [
                    {"id": 1, "date": "2024-01-01"},
                    {"id": 2, "date": "2024-03-01"},
                    {"id": 3, "date": "2024-02-01"},
                ],
                True,
                [
                    {"id": 2, "date": "2024-03-01"},
                    {"id": 3, "date": "2024-02-01"},
                    {"id": 1, "date": "2024-01-01"},
                ],
        ),
        (
                [
                    {"id": 1, "date": "2024-01-01"},
                    {"id": 2, "date": "2024-03-01"},
                    {"id": 3, "date": "2024-02-01"},
                ],
                False,
                [
                    {"id": 1, "date": "2024-01-01"},
                    {"id": 3, "date": "2024-02-01"},
                    {"id": 2, "date": "2024-03-01"},
                ],
        ),
    ],
)
def test_sort_by_date(data, descending, expected):
    assert sort_by_date(data, descending) == expected


def test_sort_by_date_default():
    data = [
        {"id": 1, "date": "2024-01-01"},
        {"id": 2, "date": "2024-03-01"},
        {"id": 3, "date": "2024-02-01"},
    ]
    expected = [
        {"id": 2, "date": "2024-03-01"},
        {"id": 3, "date": "2024-02-01"},
        {"id": 1, "date": "2024-01-01"},
    ]

    assert sort_by_date(data) == expected
