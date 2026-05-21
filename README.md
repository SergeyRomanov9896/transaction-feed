# transaction-feed

Проект `transaction-feed` предоставляет набор утилит для обработки банковских транзакций: загрузка и фильтрация операций, сортировка по дате, маскирование номеров карт и счетов, генерация номеров карт, конвертация валют и простое логирование.

## 1. Описание проекта

Этот проект содержит набор модулей для работы с банковскими операциями:

- `src/processing.py`
  - `filter_by_state` — фильтрует список операций по полю `state` (например, оставляет только `EXECUTED`).
  - `sort_by_date` — сортирует список операций по полю `date` (по умолчанию от новых к старым).
- `src/generators.py`
  - `card_number_generator` — генерирует форматированные номера карт в диапазоне чисел.
  - `filter_by_currency` — фильтрует операции по валюте платежа.
  - `transaction_descriptions` — извлекает описание из записей транзакций.
- `src/masks.py`
  - `get_mask_card_number` — маскирует 16-значный номер карты, заменяя средние 6 цифр на `*`.
  - `get_mask_account` — маскирует банковский счет, оставляя видимыми только последние 4 цифры.
- `src/widget.py`
  - `mask_account_card` — выбирает нужный метод маскировки по формату строки платежа (`Счет ...` или любой другой номер карты).
  - `get_date` — преобразует дату ISO `YYYY-MM-DDTHH:MM:SS` в формат `DD.MM.YYYY`.
- `src/utils.py`
  - `get_transactions` — загружает транзакции из JSON-файла и обрабатывает ошибки парсинга/отсутствия файла.
  - `data_filtering` — фильтрует транзакции со статусом `EXECUTED` и возвращает список с `currency` и `amount`.
- `src/external_api.py`
  - `convert_transaction_to_rubles` — конвертирует валютную транзакцию в рубли, обрабатывая `RUB`, `USD` и `EUR`.
- `src/transaction_importer.py`
  - `load_transactions_from_csv` — загружает транзакции из CSV-файла.
  - `load_transactions_from_excel` — загружает транзакции из Excel-файла.

Проект включает тесты для новых модулей:
- `tests/test_utils.py`
- `tests/test_external_api.py`
- `tests/test_transaction_importer.py`
- и другие существующие тесты для `src/decorators.py`, `src/masks.py`, `src/processing.py`, `src/generators.py`, `src/widget.py`.

## 2. Технологии и стек

- Python 3.12+
- Модульная структура в `src/`:
  - `src/processing.py`
  - `src/masks.py`
  - `src/generators.py`
  - `src/widget.py`
  - `src/decorators.py`
  - `src/utils.py`
  - `src/external_api.py`
-   - `src/transaction_importer.py`
- Тестирование: pytest
- Зависимости:
  - `python-dotenv` — для загрузки переменных окружения из `.env`
  - `requests` — для работы `src/external_api.py` с внешним API конвертации валют
-   - `pandas`, `openpyxl` — для загрузки транзакций из CSV и Excel в `src/transaction_importer.py`
- Инструменты разработки: linting, type checking и тестирование через Poetry.

## 3. Инструкция по установке

1. Клонируйте репозиторий:

```bash
git clone https://github.com/SergeyRomanov9896/transaction-feed.git
cd transaction-feed
```

2. Установите зависимости и активируйте окружение через Poetry:

```bash
poetry install
```

3. Активируйте виртуальное окружение:

```bash
poetry shell
```

4. ИЛИ запустите проект без активации оболочки:

```bash
poetry run python main.py
```

dДля работы модуля `src/external_api.py` необходимо создать файл `.env` в корне проекта со значением:

Для работы модуля `src/external_api.py` необходимо создать файл `.env` в корне проекта со значением:

```env
API_KEY=ваш_ключ
```

Если `requests` не установлен автоматически, добавьте его командой:

```bash
poetry add requests pandas openpyxl
```

## 4. Запуск тестов

Для запуска тестов используйте pytest:

```bash
poetry run pytest
```

Или с покрытием:

```bash
poetry run pytest --cov=src
```

## 5. Примеры использования

### Загрузка и фильтрация транзакций

```python
from src.utils import get_transactions, data_filtering
from src.processing import sort_by_date

transactions = get_transactions('data/operations.json')
executed = data_filtering(transactions)
sorted_executed = sort_by_date(executed)
print(sorted_executed)
```

### Загрузка транзакций из CSV и Excel

```python
from src.transaction_importer import load_transactions_from_csv, load_transactions_from_excel

csv_transactions = load_transactions_from_csv('data/transactions.csv')
excel_transactions = load_transactions_from_excel('data/transactions_excel.xlsx')

print(csv_transactions)
print(excel_transactions)
```

### Конвертация транзакций в рубли

```python
from src.external_api import convert_transaction_to_rubles

transaction = {'currency': 'USD', 'amount': '100.0'}
result = convert_transaction_to_rubles(transaction)
print(result)
```

### Маскирование карты и счета

```python
from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card

print(get_mask_card_number('1234567890123456'))
print(get_mask_account('73654108430135874305'))
print(mask_account_card('Счет 73654108430135874305'))
print(mask_account_card('Visa 1234567890123456'))
```

### Генерация номеров карт

```python
from src.generators import card_number_generator

for card_number in card_number_generator(1, 3):
    print(card_number)
```

### Обработка ошибок при маскировании

```python
from src.masks import get_mask_card_number, get_mask_account

try:
    print(get_mask_card_number('123456789012345'))
except ValueError as e:
    print(f"Ошибка: {e}")

try:
    print(get_mask_account('7365410843013587430'))
except ValueError as e:
    print(f"Ошибка: {e}")
```

### Декоратор логирования

```python
from src.decorators import log

@log(filename=None)
def process_data(data):
    return len(data)

print(process_data([1, 2, 3]))
```

### Формирование даты

```python
from src.widget import get_date
print(get_date('2025-12-31T23:59:59'))
```
