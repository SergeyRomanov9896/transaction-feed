import logging
import os

import pandas as pd
import pytest

from src.transaction_importer import load_transactions_from_csv, load_transactions_from_excel


@pytest.fixture
def valid_csv(tmp_path):
    path = tmp_path / "transactions.csv"
    path.write_text("id;amount\n1;100\n2;200\n3;150", encoding="utf-8")
    return str(path)


@pytest.fixture
def valid_excel(tmp_path):
    path = os.path.join(str(tmp_path), "transactions.xlsx")
    df = pd.DataFrame({"id": [1, 2], "amount": [100, 200]})
    df.to_excel(path, index=False)
    return path


@pytest.fixture
def empty_csv(tmp_path):
    """CSV только с заголовками (0 строк данных)"""
    path = os.path.join(str(tmp_path), "empty.csv")
    with open(path, "w", encoding="utf-8") as f:
        f.write("id,amount\n")
    return path


# ──────────────────────────────────────────────────────────────
# 1. Успешная загрузка (Happy Path)
# ──────────────────────────────────────────────────────────────
def test_csv_load_returns_list_of_dicts(valid_csv):
    result = load_transactions_from_csv(valid_csv)

    assert isinstance(result, list)
    assert len(result) == 3

    for row in result:
        assert isinstance(row, dict)

    assert result[0] == {"id": 1, "amount": 100}
    assert result[-1] == {"id": 3, "amount": 150}


# ──────────────────────────────────────────────────────────────
# 2. Обработка отсутствия файла + проверка логирования
# ──────────────────────────────────────────────────────────────
def test_csv_raises_and_logs_when_file_missing(caplog):
    caplog.set_level(logging.ERROR, logger="load_transactions")

    with pytest.raises(FileNotFoundError):
        load_transactions_from_csv("nonexistent.csv")

    assert "Файл не найден: nonexistent.csv" in caplog.text


def test_excel_raises_and_logs_when_file_missing(caplog):
    caplog.set_level(logging.ERROR, logger="load_transactions")

    with pytest.raises(FileNotFoundError):
        load_transactions_from_excel("nonexistent.xlsx")

    assert "Файл не найден: nonexistent.xlsx" in caplog.text


# ──────────────────────────────────────────────────────────────
# 3. Граничный случай: пустой файл
# ──────────────────────────────────────────────────────────────
def test_empty_csv_returns_empty_list(empty_csv):
    result = load_transactions_from_csv(empty_csv)
    assert isinstance(result, list)
    assert len(result) == 0
