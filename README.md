# transaction-feed

Проект `transaction-feed` предоставляет набор утилит для обработки банковских транзакций: фильтрация по состоянию, сортировка по дате, маскирование номеров карт и счетов, форматирование даты.

## 1. Описание проекта

Этот проект содержит простой набор функций, которые демонстрируют базовую работу с транзакциями:

- `filter_by_state` — фильтрует список операций по полю `state` (например, оставляет только `EXECUTED`).
- `sort_by_date` — сортирует список операций по полю `date` (по умолчанию от новых к старым).
- `get_mask_card_number` — маскирует 16-значный номер карты, заменяя средние 6 цифр на `*` и группируя пробелами по 4.
- `get_mask_account` — маскирует банковский счет, оставляя видимыми только последние 4 знака.
- `mask_account_card` — выбирает нужный метод маскировки в зависимости от формата строки платежа (например, `Счет ...` или `Visa ...`).
- `get_date` — превращает дату ISO `YYYY-MM-DDTHH:MM:SS` в `DD.MM.YYYY`.

## 2. Технологии и стек

- Python 3
- Модульная структура в `src/`:
  - `src/processing.py`
  - `src/masks.py`
  - `src/widget.py`
- Нет внешних зависимостей (стандартная библиотека).

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

## 3. Примеры использования

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
print(get_mask_account('4081781038221242'))      # ****1242

print(mask_account_card('Счет 4081781038221242'))
print(mask_account_card('Visa 1234567890123456'))
```

### Формирование даты

```python
from src.widget import get_date
print(get_date('2025-12-31T23:59:59'))  # 31.12.2025
```
