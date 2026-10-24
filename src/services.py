import json

from src.processing import process_bank_search


def simple_search(transactions: list[dict], query: str) -> str:
    """Ищет операции по описанию или категории и возвращает JSON."""
    result = process_bank_search(transactions, query)
    return json.dumps(result, ensure_ascii=False, indent=4)
