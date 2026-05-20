import logging

import pandas as pd

logger = logging.getLogger("load_transactions")
file_h = logging.FileHandler("logs/load_transactions.log", mode="w", encoding="utf-8")
fmt = logging.Formatter("%(asctime)s | %(filename)s | %(levelname)s | %(message)s")

file_h.setFormatter(fmt)
logger.addHandler(file_h)
logger.setLevel(logging.DEBUG)


def load_transactions_from_csv(path: str = "data/transactions.csv") -> list[dict]:
    try:
        df = pd.read_csv(path)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        logger.error("Файл не найден: %s", path)
        raise

def load_transactions_from_excel(path: str = "data/transactions_excel.xlsx") -> list[dict]:
    try:
        df = pd.read_excel(path)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        logger.error("Файл не найден: %s", path)
        raise


if __name__ == "__main__":
    print(load_transactions_from_excel())
