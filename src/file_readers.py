import pandas as pd
from pathlib import Path


def read_csv_file(file_path: str) -> list[dict]:
    """Читает CSV-файл и возвращает список словарей."""
    df = pd.read_csv(file_path, sep=";")
    return df.to_dict(orient="records")


def read_excel_file(file_path: str) -> list[dict]:
    """Читает Excel-файл и возвращает список словарей."""
    df = pd.read_excel(file_path)
    return df.to_dict(orient="records")


def read_report_csv_file(file_path: str) -> pd.DataFrame:
    """Читает CSV-файл с банковскими операциями для отчётов."""
    columns = [
        "Дата операции",
        "Дата платежа",
        "Номер карты",
        "Статус",
        "Сумма операции",
        "Валюта операции",
        "Сумма платежа",
        "Валюта платежа",
        "Кэшбэк",
        "Категория",
        "MCC",
        "Описание",
        "Бонусы (включая кэшбэк)",
        "Округление на инвесткопилку",
        "Сумма операции с округлением",
    ]

    path = Path(file_path)
    if not path.is_absolute():
        path = Path(__file__).resolve().parent.parent / path

    return pd.read_csv(
        path,
        sep=",",
        decimal=",",
        names=columns,
        header=None,
        skipinitialspace=True,
    )
