import pytest

from src.widget import get_date, mask_account_card

# ================= MASK ACCOUNT CARD =================


@pytest.mark.parametrize(
    "payment_info, expected",
    [("Visa 1234567890123456", "1234 56** **** 3456"), ("Счет 73654108430135874305", "**4305")],
)
def test_mask_account_card_parametrized(payment_info, expected):
    assert mask_account_card(payment_info) == expected


# ================= GET DATE =================


def test_converts_the_date_from_the_iso_format():
    expected = "11.03.2024"
    assert get_date("2024-03-11T02:26:18.671407") == expected


@pytest.mark.parametrize("invalid_date", [None, True, 123456789, 13.13])
def test_invalid_type_raises_type_error(invalid_date):
    with pytest.raises(AttributeError):
        get_date(invalid_date)


@pytest.mark.parametrize("invalid_date", ['', ' ', 'strange line'])
def test_incorrect_terms(invalid_date):
    with pytest.raises(IndexError):
        get_date(invalid_date)
