import pytest

from src.utils import get_transactions, process_bank_operations, process_bank_search


@pytest.fixture
def data_search():
    return [
        {"id": 1, "description": "Оплата за интернет"},
        {"id": 2, "description": "Перевод Ивану"},
        {"id": 3, "description": "Покупка в Amazon"},
        {"id": 4, "description": "Аренда квартиры"},
    ]


@pytest.fixture
def data_operations():
    return [
        {"description": "Еда"},
        {"description": "Транспорт"},
        {"description": "Еда"},
        {"description": "Еда"},
        {"description": "Развлечения"},
    ]


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


# ==========================
# 🔍 Тесты для process_bank_search
# ==========================


def test_search_exact_and_partial_match(data_search):
    result = process_bank_search(data_search, "Оплата")
    assert len(result) == 1
    assert result[0]["description"] == "Оплата за интернет"


def test_search_no_matches(data_search):
    assert process_bank_search(data_search, "Несуществующее слово") == []


def test_search_empty_data():
    assert process_bank_search([], "тест") == []


def test_search_regex_patterns():
    data = [{"description": "Сумма: 1500 руб"}, {"description": "Сумма: abc"}, {"description": "Без указания суммы"}]
    result = process_bank_search(data, r"\d+")
    assert len(result) == 1
    assert result[0]["description"] == "Сумма: 1500 руб"


def test_search_case_sensitivity(data_search):
    # По умолчанию чувствителен к регистру
    assert process_bank_search(data_search, "amazon") == []
    # Inline-флаг (?i) включает регистронезависимость
    result = process_bank_search(data_search, r"(?i)amazon")
    assert len(result) == 1


def test_search_empty_string(data_search):
    # Пустая строка в regex матчит всё
    result = process_bank_search(data_search, "")
    assert len(result) == len(data_search)


# ==========================
# 📊 Тесты для process_bank_operations
# ==========================


def test_ops_correct_counts(data_operations):
    categories = ["Еда", "Транспорт", "Развлечения"]
    result = process_bank_operations(data_operations, categories)
    assert result == {"Еда": 3, "Транспорт": 1, "Развлечения": 1}


def test_ops_missing_categories_return_zero(data_operations):
    categories = ["Еда", "Отсутствующая категория"]
    result = process_bank_operations(data_operations, categories)
    assert result == {"Еда": 3, "Отсутствующая категория": 0}


def test_ops_ignores_extra_descriptions(data_operations):
    result = process_bank_operations(data_operations, ["Еда"])
    assert result == {"Еда": 3}
    assert "Развлечения" not in result


def test_ops_empty_data():
    result = process_bank_operations([], ["Еда", "Транспорт"])
    assert result == {"Еда": 0, "Транспорт": 0}


def test_ops_empty_categories(data_operations):
    result = process_bank_operations(data_operations, [])
    assert result == {}


def test_ops_missing_description_key():
    data = [{"description": "Еда"}, {"amount": 100}]
    result = process_bank_operations(data, ["Еда"])
    assert result == {"Еда": 1}


def test_ops_duplicate_categories_in_input(data_operations):
    categories = ["Еда", "Еда", "Транспорт"]
    result = process_bank_operations(data_operations, categories)
    assert result == {"Еда": 3, "Транспорт": 1}
