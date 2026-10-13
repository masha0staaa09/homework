from unittest.mock import Mock, patch

from src.file_readers import read_csv_file, read_excel_file


@patch("src.file_readers.pd.read_csv")
def test_read_csv_file(mock_read_csv):
    mock_df = Mock()
    mock_df.to_dict.return_value = [{"id": 1, "amount": 100}]
    mock_read_csv.return_value = mock_df
    result = read_csv_file("transactions.csv")

    mock_read_csv.assert_called_once_with("transactions.csv", sep=";")
    mock_df.to_dict.assert_called_once_with(orient="records")
    assert result == [{"id": 1, "amount": 100}]


@patch("src.file_readers.pd.read_excel")
def test_read_excel_file(mock_read_excel):
    mock_df = Mock()
    mock_df.to_dict.return_value = [{"id": 1, "amount": 100}]
    mock_read_excel.return_value = mock_df
    result = read_excel_file("transactions.xlsx")

    mock_read_excel.assert_called_once_with("transactions.xlsx")
    mock_df.to_dict.assert_called_once_with(orient="records")
    assert result == [{"id": 1, "amount": 100}]
