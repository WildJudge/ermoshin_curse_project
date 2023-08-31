import pytest
import json
from utils import load_json, mask_card_number, mask_account_number, format_operation, get_last_executed_operations


@pytest.fixture
def sample_operations_data():
    """Создает и возвращает пример данных для операций"""
    data = [
        {
            "date": "2023-08-27T12:00:00.000",
            "description": "Payment",
            "operationAmount": {"amount": 100.00, "currency": {"name": "USD"}},
            "from": "1234567890123456",
            "to": "9876543210987654",
            "state": "EXECUTED"
        },
        {
            "date": "2023-08-26T12:00:00.000",
            "description": "Withdrawal",
            "operationAmount": {"amount": 50.00, "currency": {"name": "EUR"}},
            "from": "Account 9876543210",
            "to": "Account 1234567890",
            "state": "EXECUTED"
        }
    ]
    return data


def test_load_json(tmp_path):
    """Проверяет функцию загрузки JSON-файла"""
    data = {"key": "value"}
    filename = tmp_path / "test.json"
    with open(filename, "w") as f:
        json.dump(data, f)

    loaded_data = load_json(filename)
    assert loaded_data == data


def test_mask_card_number():
    """Проверяет функцию маскирования номера карты"""
    assert mask_card_number("1234567890123456") == "1234 56** **** 3456"


def test_mask_account_number():
    """Проверяет функцию маскирования номера счета"""
    assert mask_account_number("9876543210") == "**3210"


def test_format_operation():
    """Проверяет функцию форматирования операции"""
    operation = {
        "date": "2023-08-27T12:00:00.000",
        "description": "Payment",
        "operationAmount": {"amount": 100.00, "currency": {"name": "USD"}},
        "from": "1234567890123456",
        "to": "9876543210987654",
        "state": "EXECUTED"
    }
    formatted_operation = format_operation(operation)
    assert "27.08.2023 Payment" in formatted_operation


def test_get_last_executed_operations(sample_operations_data):
    """Проверяет функцию получения последних выполненных операций"""
    last_executed_operations = get_last_executed_operations(sample_operations_data, num_operations=1)
    assert "27.08.2023 Payment" in last_executed_operations
    assert "26.08.2023 Withdrawal" not in last_executed_operations
