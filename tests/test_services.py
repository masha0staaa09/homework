from src.services import simple_search


def test_simple_search_by_category():
    """Проверяет поиск операций по категории."""
    transactions = [
        {"category": "Супермаркеты", "description": "Пятёрочка"},
        {"category": "Транспорт", "description": "Такси"}
    ]

    result = simple_search(transactions, "супермаркеты")

    assert "Пятёрочка" in result
    assert "Супермаркеты" in result
    assert "Такси" not in result


def test_simple_search_by_description():
    """Проверяет поиск по описанию операции."""
    transactions = [
        {"category": "Переводы", "description": "Перевод организации"},
        {"category": "Транспорт", "description": "Такси"}
    ]

    result = simple_search(transactions, "ПЕРЕВОД")

    assert "Перевод организации" in result
    assert "Такси" not in result


def test_simple_search_no_results():
    """Проверяет результат, если совпадений нет."""
    transactions = [
        {"category": "Транспорт", "description": "Такси"}
    ]

    result = simple_search(transactions, "супермаркеты")

    assert result == "[]"
