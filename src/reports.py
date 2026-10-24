import pandas as pd
from datetime import datetime
from src.decorators import report_to_file


@report_to_file()
def spending_by_category(
        transactions: pd.DataFrame,
        category: str,
        date: str | None = None
) -> pd.DataFrame:
    """Возвращает расходы по категории за последние три месяца."""
    if date is None:
        date = datetime.today().strftime("%Y-%m-%d")

    end_date = pd.to_datetime(date)
    start_date = end_date - pd.DateOffset(months=3)

    # Работаем с копией, чтобы не менять исходные данные.
    transactions = transactions.copy()

    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"],
        dayfirst=True
    )

    transactions["Сумма операции"] = pd.to_numeric(
        transactions["Сумма операции"],
        errors="coerce"
    )

    report = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
        & (transactions["Сумма операции"] < 0)
    ]

    return report.copy()


def test_spending_by_category_saves_report(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    transactions = pd.DataFrame({
        "Дата операции": ["01.01.2022 12:00:00"],
        "Категория": ["Супермаркеты"],
        "Сумма операции": [-100.0],
    })

    spending_by_category(
        transactions,
        "Супермаркеты",
        "2022-01-15"
    )

    report_file = tmp_path / "report.txt"

    assert report_file.exists()
    assert "Супермаркеты" in report_file.read_text(encoding="utf-8")
