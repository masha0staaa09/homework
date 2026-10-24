import json
from pathlib import Path
import pandas as pd
from functools import wraps
from typing import Any, Callable


def log(filename: str | None = None) -> Callable:
    """Логирует успешное выполнение функции или возникшую ошибку."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok"

                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(message + "\n")
                else:
                    print(message)

                return result

            except Exception as error:
                message = (
                    f"{func.__name__} error: {type(error).__name__}. "
                    f"Inputs: {args}, {kwargs}"
                )

                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(message + "\n")
                else:
                    print(message)

                raise
        return wrapper
    return decorator


def report_to_file(func=None, filename="report.txt"):
    """Сохраняет результат отчёта в файл."""
    def decorator(report_func):
        @wraps(report_func)
        def wrapper(*args, **kwargs):
            result = report_func(*args, **kwargs)

            if isinstance(result, pd.DataFrame):
                content = result.to_json(
                    orient="records",
                    force_ascii=False,
                    indent=4,
                    date_format="iso",
                )
            else:
                content = json.dumps(
                    result,
                    ensure_ascii=False,
                    indent=4,
                    default=str,
                )

            Path(filename).write_text(content, encoding="utf-8")
            return result

        return wrapper

    if callable(func):
        return decorator(func)

    if isinstance(func, str):
        filename = func

    return decorator
