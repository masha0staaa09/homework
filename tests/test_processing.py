from src.processing import process_bank_operations, process_bank_search


def test_process_bank_search():
    """Проверяет поиск операций по описанию."""
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты на карту"},
    ]

    result = process_bank_search(data, "перевод")

    assert len(result) == 2
    assert result[0]["description"] == "Перевод организации"
    assert result[1]["description"] == "Перевод с карты на карту"


def test_process_bank_operations():
    """Проверяет подсчёт операций по категориям."""
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
    ]

    categories = ["Перевод организации", "Открытие вклада"]

    result = process_bank_operations(data, categories)

    assert result == {
        "Перевод организации": 2,
        "Открытие вклада": 1,
    }
