def filter_by_state(words: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список словарей по ключу «state».

    Args:
        words (list[dict]): Список словарей для фильтрации.
        state (str): Значение состояния для фильтрации. По умолчанию "EXECUTED".

    Returns:
        list[dict]: Список словарей, где ключ 'state' совпадает с заданным состоянием.
    """
    words_state = [word for word in words if word["state"] == state]
    return words_state


def sort_by_date(words: list[dict], descending: bool = True) -> list[dict]:
    """
    Сортирует список словарей по ключу «date».

    Args:
        words (list[dict]): Список словарей для сортировки.
        descending (bool): По умолчанию сортирует в порядке убывания (от новых к старым).

    Returns:
        list[dict]: Отсортированный список словарей по ключу «date».
    """
    return sorted(words, key=lambda x: x["date"], reverse=descending)
