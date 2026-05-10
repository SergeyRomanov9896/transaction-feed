import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "")
CONVERT_URL = "https://api.apilayer.com/exchangerates_data/convert"
TARGET_CURRENCY = "RUB"
SUPPORTED_CURRENCIES = {"USD", "EUR"}


def _convert_via_api(currency: str, amount: float) -> float:
    """
    Делает запрос к внешнему API /convert.
    Возвращает сконвертированную сумму в рублях.
    Выбрасывает ValueError при ошибках.
    """
    if not API_KEY:
        raise ValueError("API_KEY не найден. Создайте файл .env в корне проекта и добавьте строку: API_KEY=ваш_ключ")

    headers = {"apikey": API_KEY}
    params = {"to": TARGET_CURRENCY, "from": currency, "amount": amount}

    try:
        # timeout=10 защищает от зависания при плохом интернете
        response = requests.get(CONVERT_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("success"):
            return float(data["result"])
        else:
            error_msg = data.get("error", {}).get("message", "Неизвестная ошибка API")
            raise ValueError(f"API вернул ошибку: {error_msg}")

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Ошибка сети при запросе к API: {e}")


def convert_transaction_to_rubles(transaction: dict) -> float:
    """
    Основная функция по заданию.
    Принимает: {"currency": "USD", "amount": "8221.37"}
    Возвращает: float — сумма в рублях
    """
    currency = transaction.get("currency", "").upper()

    try:
        amount = float(transaction.get("amount", 0))
    except (ValueError, TypeError):
        raise ValueError(f"Некорректная сумма в транзакции: {transaction.get('amount')}")

    if currency == TARGET_CURRENCY:
        return round(amount, 2)

    if currency not in SUPPORTED_CURRENCIES:
        raise ValueError(f"Валюта {currency} не поддерживается для конвертации")

    result = _convert_via_api(currency, amount)
    return round(result, 2)
