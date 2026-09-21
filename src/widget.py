from src.masks import get_mask_account, get_mask_card_number
from datetime import datetime


def mask_account_card(info: str) -> str:
    """Маскирует номнр банковской карты или счета"""
    parts = info.split()
    name = " ".join(parts[:-1])
    number = parts[-1]
    if name == "Счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date: str) -> str:
    """Возвращает дату в формате ДД.ММ.ГГГГ"""
    date_obj = datetime.fromisoformat(date)
    return date_obj.strftime("%d.%m.%Y")
