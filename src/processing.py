def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция принимает список словарей и возвращает отсортированный список"""
    result = []

    for item in data:
        if item.get("state") == state:
            result.append(item)

    return result
