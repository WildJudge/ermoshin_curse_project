import json
from datetime import datetime


def load_json(filename):
    """Загружает json файл"""
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def mask_card_number(card_number):
    """Маскирует номер карты, оставляя видимыми только первые 6 и последние 4 цифры"""
    broken_number = card_number.split(" ")
    digit = broken_number[-1]
    card_number = [digit[x:x + 4] for x in range(0, len(digit), 4)]
    hide_number = f"{card_number[0]} {card_number[1][0:2]}** **** {card_number[3]}"
    broken_number[-1] = hide_number
    return " ".join(broken_number)


def mask_account_number(account_number):
    """Маскирует номер счета, оставляя видимыми только последние 4 цифры"""
    masked_number = "**" + account_number[-4:]
    return masked_number


def format_operation(operation):
    """Форматирует вывод операции согласно заданным требованиям"""
    date = datetime.strptime(operation['date'], "%Y-%m-%dT%H:%M:%S.%f")
    formatted_date = date.strftime("%d.%m.%Y")

    description = operation['description']
    amount = operation['operationAmount']['amount']
    currency = operation['operationAmount']['currency']['name']

    if 'from' in operation and operation['from']:
        from_account = operation['from']
        from_account_parts = from_account.split()
        from_account_name = from_account_parts[0]

        # Проверка, является ли первое слово в названии карты или счета числом
        if from_account_name.isdigit():
            from_account = f"Счет {mask_account_number(from_account)}"
        else:
            from_account_number = " ".join(from_account_parts[1:])  # Объединяем оставшиеся части названия в номер карты
            from_account = f"{from_account_name} {mask_card_number(from_account_number)}"

        to_account = mask_account_number(operation['to'])
        formatted_operation = f"{formatted_date} {description}\n{from_account} -> {to_account}\n{amount} {currency}\n"
    else:
        from_account = "Отсутствует"
        to_account = mask_account_number(operation['to'])
        formatted_operation = f"{formatted_date} {description}\n{from_account} -> {to_account}\n{amount} {currency}\n"

    return formatted_operation


def get_last_executed_operations(operations, num_operations=5):
    """Получает последние выполненные операции с заданным количеством операций"""
    executed_operations = [
        operation for operation in operations if operation.get('state') == 'EXECUTED' and operation
    ]
    sorted_operations = sorted(executed_operations, key=lambda x: x['date'], reverse=True)
    last_operations = sorted_operations[:num_operations]

    formatted_operations = [format_operation(operation) for operation in last_operations]
    formatted_output = "\n".join(formatted_operations)
    return formatted_output
