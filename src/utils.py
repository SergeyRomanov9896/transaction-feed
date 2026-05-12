import json
import logging

logger = logging.getLogger("transactions")
file_h = logging.FileHandler("logs/transactions.log", mode="w", encoding="utf-8")
fmt = logging.Formatter("%(asctime)s | %(filename)s | %(levelname)s | %(message)s")

file_h.setFormatter(fmt)
logger.addHandler(file_h)
logger.setLevel(logging.INFO)


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
            return data_json
    except json.JSONDecodeError as e:
        logger.error("Ошибка парсинга JSON: %s", e)
        return []
    except FileNotFoundError:
        logger.error("Файл не найден: %s", path)
        return []


def data_filtering(data: list) -> list[dict]:
    """Фильтрует транзакции по статусу EXECUTED и извлекает валюту и сумму.

    Аргументы:
        data (list): Список транзакций.

    Возвращает:
        list: Список словарей с ключами 'currency' и 'amount'.

    Вызывает:
        ValueError: Если нет транзакций со статусом EXECUTED.
    """
    if not any(ex.get("state") == "EXECUTED" for ex in data):
        logger.warning("В данных отсутствуют транзакции со статусом EXECUTED")
        raise ValueError("Ошибка валидации: в данных отсутствуют транзакции со статусом EXECUTED")

    dict_transaction = []

    for ex in data:
        if ex.get("state") != "EXECUTED":
            continue

        operation = ex.get("operationAmount")

        if not isinstance(operation, dict):
            continue

        currency = operation.get("currency", {}).get("code")
        amount = operation.get("amount")

        if currency is None or amount is None:
            continue

        dict_transaction.append({"currency": currency, "amount": amount})

    logger.info("Успешно добавлены словари с ключами currency и amount")
    return dict_transaction
