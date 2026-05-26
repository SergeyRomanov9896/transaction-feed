import json
import logging
import re

logger = logging.getLogger("transactions")
file_h = logging.FileHandler("logs/transactions.log", mode="w", encoding="utf-8")
fmt = logging.Formatter("%(asctime)s | %(filename)s | %(levelname)s | %(message)s")

file_h.setFormatter(fmt)
logger.addHandler(file_h)
logger.setLevel(logging.DEBUG)


def get_transactions(path: str = "data/operations.json") -> list:
    """Загружает транзакции из JSON-файла.

    Аргументы:
        path (str): Путь к JSON-файлу. По умолчанию "data/operations.json".

    Возвращает:
        list: Список транзакций или пустой список в случае ошибки.
    """
    try:
        with open(path, encoding="utf-8") as f:
            data_json = json.load(f)
            logger.info("Транзакции из JSON-файла успешно загружены.")
            return [item for item in data_json if item]

    except json.JSONDecodeError as e:
        logger.error("Ошибка парсинга JSON: %s", e)
        return []
    except FileNotFoundError:
        logger.error("Файл не найден: %s", path)
        return []


def extract_currency_and_amount(data: list[dict]) -> list[dict]:
    """Извлекает валюту и сумму из списка транзакций.

    Аргументы:
        data: Список словарей с информацией о транзакциях.

    Возвращает:
        Список словарей с ключами 'currency' (код валюты) и 'amount' (сумма).
    """
    dict_transaction = []

    for item in data:
        currency = item["operationAmount"]["currency"]["code"]
        amount = item["operationAmount"]["amount"]

        dict_transaction.append({"currency": currency, "amount": amount})

    logger.info("Успешно добавлены словари с ключами currency и amount")
    return dict_transaction


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Выполняет поиск транзакций по описанию с использованием регулярного выражения.

    Аргументы:
        data: Список словарей с информацией о транзакциях.
        search: Строка для поиска (регулярное выражение).

    Возвращает:
        Список транзакций, описание которых соответствует регулярному выражению.
    """
    return [item for item in data if re.search(search, item["description"])]


def process_bank_operations(data: list[dict], categories: list[str]) -> dict[str, int]:
    """Подсчитывает количество операций по категориям.

    Аргументы:
        data: Список словарей с информацией о транзакциях.
        categories: Список категорий для подсчета.

    Возвращает:
        Словарь, где ключи — это категории, а значения — количество операций в каждой категории.
    """
    number_of_operations = {}

    categories_set = set(categories)

    for transaction in data:
        description = transaction["description"]

        if description in categories_set:
            number_of_operations[description] = number_of_operations.get(description, 0) + 1

    return number_of_operations
