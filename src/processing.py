import re
from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Ищет банковские операции по строке в описании."""
from typing import Dict, List


def filter_by_state(data: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """Фильтрует список словарей по значению ключа 'state'"""
    result = []
    for transaction in data:
        description = transaction.get("description", "")

    for item in data:
        if item.get("state") == state:
            result.append(item)
        if re.search(re.escape(search), description, re.IGNORECASE):
            result.append(transaction)

    return result


def sort_by_date(data: List[Dict], descending: bool = True) -> List[Dict]:
    """Функция принимает список словарей и возвращает
     отсортированный список по дате"""
    return sorted(data, key=lambda item: item["date"], reverse=descending)
def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Подсчитывает количество операций по заданным категориям."""
    descriptions = [
        transaction.get("description", "")
        for transaction in data
    ]

    counter = Counter(descriptions)

    return {
        category: counter[category]
        for category in categories
    }
