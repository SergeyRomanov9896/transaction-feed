import os
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def log(filename: str | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Декоратор логирования выполнения функции.

    Args:
        filename (str | None): Имя файла для записи логов. Если None, вывод ведется в консоль.

    Raises:
        TypeError: Если filename не None и не является строкой.

    Returns:
        Callable: Декоратор, который оборачивает функцию и ведет лог успешного выполнения или ошибок.
    """
    if filename is not None and not isinstance(filename, str):
        raise TypeError("Ожидаемый тип данных должен быть строкой.")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            if filename:
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                log_file_path = os.path.join(base_dir, "data", filename)
                os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            else:
                log_file_path = None

            try:
                result = func(*args, **kwargs)

                if log_file_path:
                    with open(log_file_path, "a", encoding="utf-8") as f:
                        f.write(f"{func.__name__} ok\n")
                else:
                    print(f"{func.__name__} ok")
                return result
            except Exception as e:
                error_msg = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"
                if log_file_path:
                    with open(log_file_path, "a", encoding="utf-8") as f:
                        f.write(error_msg)
                else:
                    print(error_msg)
                raise

        return wrapper

    return decorator
