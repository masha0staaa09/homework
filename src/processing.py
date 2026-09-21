from typing import List, Dict


def filter_by_state(data: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """Фильтрует список словарей по значению ключа state"""
    result = []

    for item in data:
        if item.get("state") == state:
            result.append(item)

    return result


def sort_by_date(data: List[Dict], descending: bool = True) -> List[Dict]:
    """Функция принимает список словарей и возвращает
     отсортированный список по дате"""
    return sorted(data, key=lambda item: item["date"], reverse=descending)
