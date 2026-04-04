import pytest

from src.masks import get_mask_account, get_mask_card_number

# ================= GET MASK CARD NUMBER =================


def test_get_mask_card_number_valid_input_returns_masked_string():
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"


def test_get_mask_card_number_invalid_type_raises_error():
    with pytest.raises(TypeError):
        get_mask_card_number(7000792289606361)


def test_get_mask_card_number_none_input_raises_type_error():
    with pytest.raises(TypeError):
        get_mask_card_number(None)


# ================= GET MASK ACCOUNT =================


def test_get_mask_account_valid_input_returns_masked_string():
    assert get_mask_account("73654108430135874305") == "**4305"


def test_get_mask_account_invalid_type_raises_error():
    with pytest.raises(TypeError):
        get_mask_account(73654108430135874305)


def test_get_mask_account_none_input_raises_type_error():
    with pytest.raises(TypeError):
        get_mask_account(None)
