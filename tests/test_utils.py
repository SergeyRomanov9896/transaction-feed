import pytest

from src.utils import data_filtering, get_transactions

# ================= GET TRANSACTIONS =================


def test_parsing_error(tmp_path, capsys):
    bad_file = tmp_path / "operations.json"
    bad_file.write_text("{ invalid json }")
    get_transactions(str(bad_file))

    capture = capsys.readouterr()
    assert "Ошибка парсинга JSON: " in capture.out


def test_file_not_found(tmp_path):
    config_path = tmp_path / "operations.json"

    result = get_transactions(str(config_path))
    assert result == []


# ================= DATA FILTERING =================

def test_valid_data_returns_correct_result():
    """✅ Счастливый путь: валидные EXECUTED транзакции"""
    data = [
        {"state": "EXECUTED", "operationAmount": {"amount": 1500.50, "currency": {"code": "RUB"}}},
        {"state": "EXECUTED", "operationAmount": {"amount": 200, "currency": {"code": "USD"}}}
    ]
    result = data_filtering(data)
    assert result == [
        {"currency": "RUB", "amount": 1500.50},
        {"currency": "USD", "amount": 200}
    ]


def test_no_executed_transactions_raises_error():
    data = [
        {"state": "PENDING"},
        {"state": "CANCELED"}
    ]
    with pytest.raises(ValueError, match="отсутствуют транзакции со статусом EXECUTED"):
        data_filtering(data)

