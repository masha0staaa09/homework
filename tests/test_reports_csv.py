from src.file_readers import read_report_csv_file


def test_read_report_csv_file():
    df = read_report_csv_file("data/reports.csv")
    assert not df.empty
    assert "Дата операции" in df.columns
    assert "Категория" in df.columns
