import re

from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.transaction_importer import load_transactions_from_csv, load_transactions_from_excel
from src.utils import get_transactions, process_bank_search

VALID_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def _format_and_print_transactions(transactions: list[dict]) -> None:
    """Форматирует и выводит транзакции в читаемом виде."""
    if not transactions:
        print("\nПрограмма: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации\n")
        return

    print("\nПрограмма:")
    print(f"Всего банковских операций в выборке: {len(transactions)}\n")

    for tx in transactions:
        date = tx.get("date", tx.get("operationDate", "Не указана"))[:10]
        description = tx.get("description", tx.get("name", "Без описания"))
        print(f"{date} {description}")

        from_account = tx.get("from", tx.get("fromAccount", ""))
        to_account = tx.get("to", tx.get("toAccount", ""))

        if from_account and to_account:
            print(f"{from_account} -> {to_account}")
        elif from_account:
            print(from_account)
        elif to_account:
            print(to_account)

        amount = tx.get("amount", tx.get("operationAmount", {}).get("amount", "0"))
        currency = tx.get(
            "currency", tx.get("currency_code", tx.get("operationAmount", {}).get("currency", {}).get("code", ""))
        )

        if isinstance(amount, (int, float)):
            amount = int(amount) if amount == int(amount) else amount

        if currency and currency.upper() == "RUB":
            print(f"Сумма: {amount} руб.")
        elif currency:
            print(f"Сумма: {amount} {currency}")
        else:
            print(f"Сумма: {amount}")

        print()


def _process_transactions(transactions) -> None:
    """
    Управляет потоком фильтрации и вывода транзакций для CLI.

    Последовательно запрашивает у пользователя:
    1. Статус операции
    2. Сортировку по дате
    3. Фильтрацию по валюте (RUB)
    4. Поиск по описанию

    Args:
        transactions: Исходный список транзакций из файла.

    Side Effects:
        Выводит результаты в консоль или сообщения об отсутствии данных.
        Завершает выполнение функции через return при пустой выборке.
    """
    while True:
        status = input("Введите статус (EXECUTED, CANCELED, PENDING): ").upper().strip()
        if status not in VALID_STATUSES:
            print(f"Недопустимый статус. Доступные: {', '.join(sorted(VALID_STATUSES))}\n")
            continue

        filtered = filter_by_state(transactions, status)
        if not filtered:
            print(f'Транзакций со статусом "{status}" не найдено.\n')
            continue
        break

    sort_choice = input("Отсортировать операции по дате? (Да/Нет): ").strip().lower()
    if sort_choice == "да":
        direction = input("По возрастанию или по убыванию?: ").strip().lower()
        ascending = "возрастанию" in direction
        filtered = sort_by_date(filtered, ascending)

    rub_only = input("Выводить только рублевые транзакции? (Да/Нет): ").strip().lower()
    if rub_only == "да":
        filtered = list(filter_by_currency(filtered, currency="RUB"))
        if not filtered:
            print("Рублевых транзакций не найдено. Возврат в меню.\n")
            return

    search_choice = (
        input("Отфильтровать список транзакций по определенному слову в описании? (Да/Нет): ").strip().lower()
    )
    if search_choice == "да":
        search_word = input("Введите слово или фразу для поиска: ").strip()
        if search_word:
            filtered = process_bank_search(filtered, re.escape(search_word))
            if not filtered:
                print(f'Транзакций с описанием, содержащим "{search_word}", не найдено. Возврат в меню.\n')
                return
        else:
            print("Поисковый запрос пуст. Пропускаем фильтрацию.\n")

    _format_and_print_transactions(filtered)


def handle_json():
    print("Для обработки выбран JSON-файл.\n")
    _process_transactions(get_transactions())


def handle_csv():
    print("Для обработки выбран CSV-файл.\n")
    _process_transactions(load_transactions_from_csv())


def handle_xlsx():
    print("Для обработки выбран XLSX-файл.\n")
    _process_transactions(load_transactions_from_excel())


def main() -> None:
    """
    Точка входа в программу.
    Отображает меню выбора формата файла и запускает обработку.
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n")

    menu = {1: handle_json, 2: handle_csv, 3: handle_xlsx}

    while True:
        print("Выберите пункт меню:")
        print("1. JSON  2. CSV  3. XLSX")
        try:
            choice = int(input("Ввод: "))
            if choice in menu:
                menu[choice]()
                break
            print("Такого пункта нет. Попробуйте снова.\n")
        except ValueError:
            print("Введите число от 1 до 3.\n")


if __name__ == "__main__":
    main()
