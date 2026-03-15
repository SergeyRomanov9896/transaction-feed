from masks import get_mask_account, get_mask_card_number


def mask_account_card(payment_info: str) -> str:
    """
    Маскирует номер счета или карты в строке информации о платеже.

    Args:
        payment_info (str): Строка, содержащая тип платежа («Счет» для имени счета или карты) и номер, разделенные пробелом.

    Returns:
        str: Маскированная версия номера счета или карты.
    """
    words = payment_info.rsplit(" ", 1)
    name = words[0]
    number = words[1]

    if name == "Счет":
        return get_mask_account(number)
    return get_mask_card_number(number)





