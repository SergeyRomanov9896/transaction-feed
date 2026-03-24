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


