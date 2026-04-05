def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер кредитной карты, заменяет 6 средних цифр на звездочки.
    Преобразует 16-значный номер карты в форматированную строку с замаскированными цифрами.

    Args:
        card_number (str): 16-значный номер кредитной карты.

    Returns:
        str: Замаскированный номер карты, отформатированный с пробелами в группах по 4 цифры.
    """
    if len(card_number) != 16:
        raise ValueError("Нестандартное количество цифр")

    number_disguise = card_number[6:12]
    disguise = card_number.replace(number_disguise, "******")
    separation = disguise[0:4] + " " + disguise[4:8] + " " + disguise[8:12] + " " + disguise[-4:]
    return separation


def get_mask_account(account: str) -> str:
    """
    Маскирует номер банковского счета, заменяя все символы, кроме последних четырех, на звездочки.

    Args:
        account (str): Номер банковского счета в виде строки.
    Returns:
        str: Замаскированный номер счета, где все символы, кроме последних четырех заменены на звездочки.
    """
    if len(account) != 20:
        raise ValueError("Нестандартное количество цифр")

    number_disguise = account[14:16]
    disguise = account.replace(number_disguise, "**")
    return disguise[-6:]
