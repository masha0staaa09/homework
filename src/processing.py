def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция принимает список словарей и возвращает отсортированный список по ключу"""
    result = []

    for item in data:
        if item.get("state") == state:
            result.append(item)

    return result


def sort_by_date(data: list[dict], descending: bool = True) -> list[dict]:
    """Функция принимает список словарей и возвращает отсортированный список по дате"""
    return sorted(data, key=lambda item: item["date"], reverse=descending)
