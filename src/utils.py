import json


def get_transactions(path: str = "data/operations.json") -> None | list:
    """Загружает транзакции из JSON-файла.

    Аргументы:
        path (str): Путь к JSON-файлу. По умолчанию "data/operations.json".

    Возвращает:
        list: Список транзакций или пустой список в случае ошибки.
    """
    try:
        with open(path, encoding="utf-8") as f:
            data_json = json.load(f)
            return data_json
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
        return []
    except FileNotFoundError:
        print("Файл не найден")
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

    return dict_transaction
