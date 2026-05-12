import logging

logger = logging.getLogger("get_card")
file_h = logging.FileHandler("logs/get_card.log", mode="w", encoding="utf-8")
fmt = logging.Formatter("%(asctime)s | %(filename)s | %(levelname)s | %(message)s")

file_h.setFormatter(fmt)
logger.addHandler(file_h)
logger.setLevel(logging.INFO)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер кредитной карты, заменяет 6 средних цифр на звездочки.
    Преобразует 16-значный номер карты в форматированную строку с замаскированными цифрами.

    Args:
        card_number (str): 16-значный номер кредитной карты.

    Raises:
        ValueError: Если длина номера карты не равна 16 символам.

    Returns:
        str: Замаскированный номер карты, отформатированный с пробелами в группах по 4 цифры.
    """
    if len(card_number) != 16:
        logger.warning("Нестандартное количество цифр в номере карты: %s", card_number)
        raise ValueError("Нестандартное количество цифр")

    logger.info("Номер карты успешно замаскирован: %s...", card_number[:4])
    return f"{card_number[0:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account: str) -> str:
    """
    Маскирует номер банковского счета, заменяя все символы, кроме последних четырех, на звездочки.

    Args:
        account (str): Номер банковского счета в виде строки.

    Raises:
        ValueError: Если длина номера счета не равна 20 символам.

    Returns:
        str: Замаскированный номер счета, где все символы, кроме последних четырех заменены на звездочки.
    """
    if len(account) != 20:
        logger.warning("Нестандартное количество цифр в номере банковского счета: %s", account)
        raise ValueError("Нестандартное количество цифр")

    logger.info("Номер счета успешно замаскирован **%s", account[-4:])
    return f"**{account[-4:]}"
