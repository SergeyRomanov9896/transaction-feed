import pytest

from src.masks import get_mask_account, get_mask_card_number

# ================= GET MASK CARD NUMBER =================


def test_get_mask_card_number_valid_input_returns_masked_string():
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"


@pytest.mark.parametrize("invalid_input", [7000792289606361, None, 12.34, True])
def test_get_mask_card_number_invalid_type_raises_type_error(invalid_input):
    with pytest.raises(TypeError):
        get_mask_card_number(invalid_input)


@pytest.mark.parametrize("invalid_card", ["700079228960636100", "7000792289606"])
def test_number_does_not_exceed_the_specified_range(invalid_card):
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_card)


# ================= GET MASK ACCOUNT =================


def test_get_mask_account_valid_input_returns_masked_string():
    assert get_mask_account("73654108430135874305") == "**4305"


@pytest.mark.parametrize("invalid_input", [73654108430135874305, None, 12.34, True])
def test_get_mask_account_invalid_type_raises_type_error(invalid_input):
    with pytest.raises(TypeError):
        get_mask_account(invalid_input)


@pytest.mark.parametrize("invalid_card", ["736541084301358743051234", "73654108430"])
def test_account_does_not_exceed_the_specified_range(invalid_card):
    with pytest.raises(ValueError):
        get_mask_account(invalid_card)
