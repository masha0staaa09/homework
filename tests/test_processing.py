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


def test_process_bank_search_by_category():
    """Проверяет поиск операций по категории."""
    data = [
        {"category": "Супермаркеты", "description": "Пятёрочка"},
        {"category": "Транспорт", "description": "Такси"},
    ]

    result = process_bank_search(data, "супермаркеты")

    assert len(result) == 1
    assert result[0]["description"] == "Пятёрочка"


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


def test_process_bank_search_case_insensitive():
    """Проверяет поиск без учёта регистра и все совпадения."""
    data = [
        {"description": "Перевод организации"},
        {"description": "ПЕРЕВОД по номеру"},
        {"description": "Оплата покупки"},
        {"description": "Перевод с карты на карту"},
    ]
    result = process_bank_search(data, "перевод")

    assert len(result) == 3
    assert all("перевод" in item["description"].lower() for item in result)
