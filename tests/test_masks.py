import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_masking_numbers():
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"
    assert get_mask_account("73654108430135874305") == "**4305"


def test_invalid_data_type_card():
    with pytest.raises((TypeError, IndexError)):
        get_mask_card_number(7000792289606361)


def test_invalid_data_type_account():
    with pytest.raises((TypeError, IndexError)):
        get_mask_account(73654108430135874305)


def test_card_with_none():
    with pytest.raises(TypeError):
        get_mask_card_number(None)


def test_account_with_none():
    with pytest.raises(TypeError):
        get_mask_account(None)
