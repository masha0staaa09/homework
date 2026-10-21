import pandas as pd


def read_csv_file(file_path: str) -> list[dict]:
    """Читает CSV-файл и возвращает список словарей."""
    df = pd.read_csv(file_path, sep=";")
    return df.to_dict(orient="records")


def read_excel_file(file_path: str) -> list[dict]:
    """Читает Excel-файл и возвращает список словарей."""
    df = pd.read_excel(file_path)
    return df.to_dict(orient="records")
