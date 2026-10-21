import pandas as pd

from src.file_readers import read_csv_file, read_excel_file


def test_read_csv_file(tmp_path):
    """Проверяет чтение CSV-файла."""
    file_path = tmp_path / "test.csv"
    df = pd.DataFrame([
        {"description": "Перевод", "amount": 100},
        {"description": "Покупка", "amount": 200},
    ])
    df.to_csv(file_path, sep=";", index=False)
    result = read_csv_file(str(file_path))

    assert len(result) == 2
    assert result[0]["description"] == "Перевод"
    assert result[0]["amount"] == 100


def test_read_excel_file(tmp_path):
    """Проверяет чтение Excel-файла."""
    file_path = tmp_path / "test.xlsx"
    df = pd.DataFrame([
        {"description": "Перевод", "amount": 100},
        {"description": "Покупка", "amount": 200},
    ])
    df.to_excel(file_path, index=False)
    result = read_excel_file(str(file_path))

    assert len(result) == 2
    assert result[0]["description"] == "Перевод"
    assert result[0]["amount"] == 100
