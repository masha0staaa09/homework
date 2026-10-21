import pytest

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
