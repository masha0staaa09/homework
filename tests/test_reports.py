import pandas as pd
from src.file_readers import read_report_csv_file
from src.reports import spending_by_category


def test_spending_by_category():
    transactions = read_report_csv_file("data/reports.csv")
    result = spending_by_category(
        transactions,
        "Супермаркеты",
        "2022-01-15"
    )

    print("\nНайденные операции:")
    print(result[["Дата операции", "Категория", "Сумма операции"]].head(5))

    assert all(result["Категория"] == "Супермаркеты")
    assert all(result["Сумма операции"] < 0)
    assert all(result["Дата операции"] >= "2021-10-15")
    assert all(result["Дата операции"] <= "2022-01-15")


def test_spending_by_category_no_results():
    transactions = pd.DataFrame({
        "Дата операции": ["01.01.2022 12:00:00"],
        "Категория": ["Транспорт"],
        "Сумма операции": [-100.0],
    })
    result = spending_by_category(
        transactions,
        "Супермаркеты",
        "2022-01-15"
    )

    assert result.empty


def test_spending_by_category_does_not_change_input():
    transactions = pd.DataFrame({
        "Дата операции": ["01.01.2022 12:00:00"],
        "Категория": ["Супермаркеты"],
        "Сумма операции": [-100.0],
    })
    original = transactions.copy(deep=True)

    spending_by_category(
        transactions,
        "Супермаркеты",
        "2022-01-15"
    )

    pd.testing.assert_frame_equal(transactions, original)


def test_spending_by_category_uses_current_date():
    transactions = pd.DataFrame({
        "Дата операции": ["01.10.2026 12:00:00"],
        "Категория": ["Супермаркеты"],
        "Сумма операции": [-100.0],
    })
    result = spending_by_category(
        transactions,
        "Супермаркеты"
    )

    assert len(result) == 1
