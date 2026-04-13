from collections.abc import Iterator


def filter_by_currency(data: list[dict], currency="USD") -> Iterator[dict]:
    """
    Фильтрует список словарей транзакций по указанной валюте.

    Args:
        data (list[dict]): Список словарей транзакций, каждый содержащий ключ 'operationAmount' с информацией о валюте.
        currency (str): Название валюты для фильтрации (например, "USD", "RUB"). По умолчанию "USD".

    Yields:
        dict: Словари транзакций, где валюта соответствует указанной валюте.
    """
    yield from [i for i in data if i["operationAmount"]["currency"]["name"] == currency]


def transaction_descriptions(data: list[dict]) -> Iterator[str]:
    """
    Извлекает и возвращает описания из списка словарей транзакций.

    Args:
        data (list[dict]): Список словарей транзакций, каждый потенциально содержащий ключ 'description'.

    Yields:
        str: Строки описаний из транзакций.
    """
    yield from [i["description"] for i in data if i["description"]]


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генерирует отформатированные номера карт как строки из диапазона целых чисел.

    Args:
        start (int): Начальное целое число для генерации номера карты.
        stop (int): Конечное целое число для генерации номера карты (включительно).

    Yields:
        str: Отформатированные номера карт в формате "XXXX XXXX XXXX XXXX".
    """
    for i in range(start, stop + 1):
        full_number = str(i).zfill(16)
        yield f"{full_number[0:4]} {full_number[4:8]} {full_number[8:12]} {full_number[12:]}"
