# transaction-feed

Проект `transaction-feed` предоставляет набор утилит для обработки банковских транзакций: фильтрация по состоянию, сортировка по дате, маскирование номеров карт и счетов, генерация номеров карт и форматирование даты.

## 1. Описание проекта

Этот проект содержит простой набор функций, которые демонстрируют базовую работу с транзакциями:

- `filter_by_state` — фильтрует список операций по полю `state` (например, оставляет только `EXECUTED`).
- `sort_by_date` — сортирует список операций по полю `date` (по умолчанию от новых к старым).
- `filter_by_currency` — фильтрует список операций по валюте платежа.
- `transaction_descriptions` — извлекает текстовые описания из записей транзакций.
- `card_number_generator` — генерирует форматированные номера карт в диапазоне чисел.
- `get_mask_card_number` — маскирует 16-значный номер карты, заменяя средние 6 цифр на `*` и группируя пробелами по 4. Включает валидацию входных данных (проверка на 16 цифр).
- `get_mask_account` — маскирует банковский счет, оставляя видимыми только последние 4 знака. Включает валидацию входных данных (проверка на 20 цифр).
- `mask_account_card` — выбирает нужный метод маскировки в зависимости от формата строки платежа (например, `Счет ...` или `Visa ...`).
- `get_date` — превращает дату ISO `YYYY-MM-DDTHH:MM:SS` в `DD.MM.YYYY`.

Проект включает полный набор тестов pytest для всех модулей, обеспечивающих надежность и корректность работы функций.

## 2. Технологии и стек

- Python 3.12+
- Модульная структура в `src/`:
  - `src/processing.py`
  - `src/masks.py`
  - `src/generators.py`
  - `src/widget.py`
- Тестирование: pytest
- Нет внешних зависимостей (стандартная библиотека), дополнительные инструменты для разработки (linting, type checking) и тестирования.

## 3. Инструкция по установке

1. Клонируйте репозиторий:

```bash
git clone https://github.com/SergeyRomanov9896/transaction-feed.git

cd transaction-feed
```

2. Установите зависимости и активируйте окружение через Poetry:

   ### Установка зависимостей (создаст окружение автоматически)

   ```bash
   poetry install
   ```

   ### Активация виртуального окружения

   ```bash
   poetry shell
   ```

   ### ИЛИ запуск проекта без активации оболочки

   ```bash
   poetry run python main.py
   ```

> В проекте нет новых внешних зависимостей: используется стандартная библиотека Python, а для тестирования применяется `pytest`.

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

### Фильтрация и сортировка операций

```python
from src.processing import filter_by_state, sort_by_date

transactions = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2024-01-01T12:00:00'},
    {'id': 2, 'state': 'PENDING', 'date': '2024-01-02T12:00:00'},
    {'id': 3, 'state': 'EXECUTED', 'date': '2024-01-03T12:00:00'},
]

executed = filter_by_state(transactions, 'EXECUTED')
sorted_executed = sort_by_date(executed)
print(sorted_executed)
```

### Маскирование карты и счета

```python
from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card

print(get_mask_card_number('1234567890123456'))  # 1234 56** **** 3456
print(get_mask_account('73654108430135874305'))      # ****1242

print(mask_account_card('Счет 73654108430135874305'))
print(mask_account_card('Visa 1234567890123456'))
```

### Генерация номеров карт

```python
from src.generators import card_number_generator

for card_number in card_number_generator(1, 3):
    print(card_number)
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
```

### Обработка ошибок при маскировании

```python
from src.masks import get_mask_card_number, get_mask_account

try:
    print(get_mask_card_number('123456789012345'))  # Недостаточно цифр
except ValueError as e:
    print(f"Ошибка: {e}")  # Ошибка: Нестандартное количество цифр

try:
    print(get_mask_account('7365410843013587430'))  # Недостаточно цифр
except ValueError as e:
    print(f"Ошибка: {e}")  # Ошибка: Нестандартное количество цифр
```

### Формирование даты

```python
from src.widget import get_date
print(get_date('2025-12-31T23:59:59'))  # 31.12.2025
```
