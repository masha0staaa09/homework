from src.file_readers import read_csv_file, read_excel_file
from src.processing import process_bank_search
from src.utils import read_json_file


def main():
    """Запускает программу обработки банковских операций."""
    print("Выберите формат файла:")
    print("1. JSON")
    print("2. CSV")
    print("3. XLSX")
    choice = input("Введите номер формата: ")

    if choice == "1":
        file_path = input("Введите путь к JSON-файлу: ")
        transactions = read_json_file(file_path)
    elif choice == "2":
        file_path = input("Введите путь к CSV-файлу: ")
        transactions = read_csv_file(file_path)
    elif choice == "3":
        file_path = input("Введите путь к XLSX-файлу: ")
        transactions = read_excel_file(file_path)
    else:
        print("Неверный выбор формата.")
        return

    print(f"Загружено операций: {len(transactions)}")
    while True:
        status = input(
            "Введите статус операции "
            "(EXECUTED, CANCELED, PENDING): "
        ).upper()

        if status in ("EXECUTED", "CANCELED", "PENDING"):
            break

        print("Неверный статус. Попробуйте ещё раз.")

    transactions = [
        transaction
        for transaction in transactions
        if str(transaction.get("state", "")).upper() == status
    ]

    print(f"Операций со статусом {status}: {len(transactions)}")

    sort_by_date = input(
        "Отсортировать операции по дате? (да/нет): "
    ).lower()

    if sort_by_date == "да":
        order = input(
            "По возрастанию или убыванию? "
            "(возрастание/убывание): "
        ).lower()

        transactions.sort(
            key=lambda transaction: transaction.get("date", ""),
            reverse=(order == "убывание")
        )

    only_rub = input(
        "Выводить только рублёвые операции? (да/нет): "
    ).lower()

    if only_rub == "да":
        transactions = [
            transaction
            for transaction in transactions
            if transaction.get("currency_code") == "RUB"
        ]

    search_by_description = input(
        "Искать операции по описанию? (да/нет): "
    ).lower()

    if search_by_description == "да":
        search = input("Введите строку для поиска: ")
        transactions = process_bank_search(
            transactions, search
        )

    if transactions:
        for transaction in transactions:
            print(transaction)
    else:
        print("Операции не найдены.")


if __name__ == "__main__":
    main()
