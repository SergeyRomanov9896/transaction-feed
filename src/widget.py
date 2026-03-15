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


def get_date(date: str) -> str:
    """
    Преобразует дату из формата ISO в формат DD.MM.YYYY.

    Args:
        date (str): Дата в формате ISO, например "2023-01-01T12:00:00".

    Returns:
        str: Дата в формате DD.MM.YYYY, например "01.01.2023".
    """
    date_and_time = date.split("T")
    year_month_day = date_and_time[0].split("-")
    new_date = f"{year_month_day[2]}.{year_month_day[1]}.{year_month_day[0]}"
    return new_date
