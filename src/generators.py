def filter_by_currency(transactions, currency):
    """Возвращаем транзакции с указанным кодом валюты."""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions):
    """Возвращает описания транзакций по одному."""
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start, stop):
    """Генерирует номера карт в формате ХХХХ ХХХХ ХХХХ ХХХХ."""
    for number in range(start, stop + 1):
        card_number = str(number).zfill(16)
        yield " ".join(
            card_number[i:i + 4] for i in range(0, 16, 4)
        )
