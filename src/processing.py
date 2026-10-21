import re
from collections import Counter
from typing import Dict, List


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Ищет банковские операции по строке в описании."""
    result = []
    for transaction in data:
        description = transaction.get("description", "")

        if re.search(re.escape(search), description, re.IGNORECASE):
            result.append(transaction)

    return result


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


def sort_by_date(data: List[Dict], descending: bool = True) -> List[Dict]:
    """Функция принимает список словарей и возвращает
     отсортированный список по дате"""
    return sorted(data, key=lambda item: item["date"], reverse=descending)
