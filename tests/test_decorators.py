import pytest
import pandas as pd
from src.decorators import report_to_file
from src.decorators import log


def test_log_success_console(capsys):
    """Проверяет успешное выполнение функции с выводом в консоль."""
    @log()
    def add(a, b):
        return a + b

    result = add(1, 2)

    captured = capsys.readouterr()

    assert result == 3
    assert captured.out == "add ok\n"


def test_log_error_console(capsys):
    """Проверяет вывод ошибки и входных параметров в консоль."""
    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()

    assert (
        "divide error: ZeroDivisionError. Inputs: (1, 0), {}"
        in captured.out
    )


def test_log_success_file(tmp_path):
    """Проверяет запись успешного выполнения в файл."""
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def add(a, b):
        return a + b

    result = add(2, 3)

    assert result == 5
    assert log_file.read_text(encoding="utf-8") == "add ok\n"


def test_log_error_file(tmp_path):
    """Проверяет запись ошибки и аргументов в файл."""
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    content = log_file.read_text(encoding="utf-8")

    assert content == "divide error: ZeroDivisionError. Inputs: (1, 0), {}\n"


def test_report_to_file_default_name(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    @report_to_file()
    def make_report():
        return {"Категория 1": 1000}

    result = make_report()

    assert result == {"Категория 1": 1000}
    assert (tmp_path / "report.txt").exists()
    assert "Категория 1" in (
        tmp_path / "report.txt"
    ).read_text(encoding="utf-8")


def test_report_to_file_custom_name(tmp_path):
    report_path = tmp_path / "custom_report.json"

    @report_to_file(str(report_path))
    def make_report():
        return {"Категория 1": 1000}

    make_report()

    assert report_path.exists()
    assert "1000" in report_path.read_text(encoding="utf-8")


def test_report_to_file_dataframe(tmp_path):
    report_path = tmp_path / "dataframe_report.txt"

    @report_to_file(str(report_path))
    def make_report():
        return pd.DataFrame({
            "Категория": ["Супермаркеты"],
            "Сумма": [-100],
        })

    result = make_report()

    assert len(result) == 1
    assert "Супермаркеты" in report_path.read_text(encoding="utf-8")


def test_report_to_file_without_parentheses(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    @report_to_file
    def make_report():
        return {"Категория": 100}

    make_report()

    report_file = tmp_path / "report.txt"

    assert report_file.exists()
    assert "Категория" in report_file.read_text(encoding="utf-8")
