from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_transaction_to_rubles


def test_rub_transaction_returns_as_is():
    tx = {"currency": "RUB", "amount": "100.50"}
    result = convert_transaction_to_rubles(tx)
    assert result == 100.50


@patch("src.external_api.requests.get")
def test_usd_conversion_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"success": True, "result": 9245.0}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    tx = {"currency": "USD", "amount": "100.0"}
    result = convert_transaction_to_rubles(tx)

    assert result == 9245.0
    mock_get.assert_called_once()


@patch("src.external_api.requests.get")
def test_api_error_raises_value_error(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"success": False, "error": {"message": "Invalid API key"}}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    tx = {"currency": "EUR", "amount": "50.0"}
    with pytest.raises(ValueError, match="API вернул ошибку"):
        convert_transaction_to_rubles(tx)


def test_unsupported_currency_raises_error():
    tx = {"currency": "CNY", "amount": "100.0"}
    with pytest.raises(ValueError, match="не поддерживается"):
        convert_transaction_to_rubles(tx)
