from src.utils import get_transactions

# ================= GET TRANSACTIONS =================


def test_parsing_error(tmp_path, caplog):
    bad_file = tmp_path / "operations.json"
    bad_file.write_text("{ invalid json }")
    get_transactions(str(bad_file))

    assert "Ошибка парсинга JSON: " in caplog.text


def test_file_not_found(tmp_path):
    config_path = tmp_path / "operations.json"

    result = get_transactions(str(config_path))
    assert result == []
