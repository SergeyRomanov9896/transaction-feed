import pytest

from src.decorators import log


def test_log_to_file(tmp_path):
    @log(filename="test_run.log", log_dir=str(tmp_path))
    def my_function():
        return "success"

    my_function()
    log_file = tmp_path / "data" / "test_run.log"
    assert log_file.read_text(encoding="utf-8") == "my_function ok\n"


def test_output_to_console_on_success(capsys):
    @log(filename=None)
    def my_function():
        return "success"

    my_function()
    captured = capsys.readouterr()
    assert captured.out == f"{my_function.__name__} ok\n"


def test_output_to_console_on_error(capsys):
    @log(filename=None)
    def my_function(x, y):
        raise ValueError("Тестовая ошибка")

    with pytest.raises(ValueError):
        my_function(x=5, y="5")

    captured = capsys.readouterr()

    expected = f"{my_function.__name__} error: ValueError. Inputs: (), {{'x': 5, 'y': '5'}}\n\n"
    assert captured.out == expected


@pytest.mark.parametrize("invalid_name", [123, 12.44, True, ["one", "two"], ("one", "two"), {1: "one"}])
def test_invalid_filename_type(invalid_name):
    with pytest.raises(TypeError, match="Ожидаемый тип данных должен быть строкой."):
        log(filename=invalid_name)
