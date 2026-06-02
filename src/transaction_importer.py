import logging

import pandas as pd

logger = logging.getLogger("load_transactions")
file_h = logging.FileHandler("logs/load_transactions.log", mode="w", encoding="utf-8")
fmt = logging.Formatter("%(asctime)s | %(filename)s | %(levelname)s | %(message)s")

file_h.setFormatter(fmt)
logger.addHandler(file_h)
logger.setLevel(logging.DEBUG)


def load_transactions_from_csv(path: str = "data/transactions.csv") -> list[dict]:
    """Загрузить транзакции из CSV-файла.

    Args:
        path: Путь к CSV-файлу.

    Returns:
        Список словарей, где каждый словарь соответствует одной транзакции.

    Raises:
        FileNotFoundError: Если файл не найден.
    """
    try:
        df = pd.read_csv(
            path,
            sep=";",
            skip_blank_lines=True,
            encoding="utf-8",
        )
        df = df.dropna(how="all")

        return df.to_dict(orient="records")
    except FileNotFoundError:
        logger.error("Файл не найден: %s", path)
        raise


def load_transactions_from_excel(path: str = "data/transactions_excel.xlsx") -> list[dict]:
    """Загрузить транзакции из Excel-файла.

    Args:
        path: Путь к Excel-файлу.

    Returns:
        Список словарей транзакций. Все NaN заменены на None,
        а поле 'description' гарантированно является строкой.

    Raises:
        FileNotFoundError: Если файл не найден.
    """
    try:
        df = pd.read_excel(path)

        if df.empty:
            logger.warning("Файл Excel пуст: %s", path)
            return []

        # 1. Гарантируем, что в колонке description всегда строка.
        #    Пустые ячейки превращаются в "", числа -> в строковое представление.
        if "description" in df.columns:
            df["description"] = df["description"].fillna("").astype(str)

        # 2. Заменяем все остальные NaN (тип float) на None.
        #    Это предотвращает TypeError в downstream-коде и упрощает сериализацию.
        df = df.where(pd.notna(df), None)

        return df.to_dict(orient="records")

    except FileNotFoundError:
        logger.error("Файл не найден: %s", path)
        raise
    except Exception as e:
        logger.error("Ошибка при чтении Excel %s: %s", path, e)
        raise
