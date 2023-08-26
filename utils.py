import json
from datetime import datetime


def load_json(filename):
    """Загружает json файл"""
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def mask_card_number(card_number):
    """Маскирует номер карты, оставляя видимыми только первые 6 и последние 4 цифры"""
    masked_number = f"{' '.join([card_number[i:i + 4] for i in range(0, len(card_number), 4)])[:-4]} XX** **** {' '.join(card_number[-4:])}"
    return masked_number


def mask_account_number(account_number):
    """Маскирует номер счета, оставляя видимыми только последние 4 цифры"""
    masked_number = "**" + account_number[-4:]
    return masked_number


def format_operation(operation):
    """Форматирует информацию об операции в заданном формате"""
    operation_date = datetime.strptime(operation['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
    from_field = operation.get('from', '')
    to_field = operation.get('to', '')

    operation_amount = f"{operation['operationAmount']['amount']} {operation['operationAmount']['currency']['name']}"

    masked_from = from_field
    masked_to = f"Счет {mask_account_number(to_field)}"

    if 'card' in from_field.lower():
        card_info = from_field.split()
        card_type = card_info[0]
        card_digits = card_info[-1]
        masked_card = f"{card_type} {card_digits[:4]} {' '.join([card_digits[4:6], '**', '****', card_digits[-4:]])}"
        masked_from = masked_card

    formatted_operation = f"{operation_date} {operation['description']}\n"
    formatted_operation += f"{masked_from} -> {masked_to}\n"
    formatted_operation += f"{operation_amount}\n"

    return formatted_operation


def get_last_executed_operations(operations, num_operations=5):
    """Получает последние выполненные операции с заданным количеством операций"""
    executed_operations = [operation for operation in operations if operation.get('state') == 'EXECUTED']
    sorted_operations = sorted(executed_operations, key=lambda x: x['date'], reverse=True)
    last_operations = sorted_operations[:num_operations]

    formatted_operations = [format_operation(operation) for operation in last_operations]
    formatted_output = "\n\n".join(formatted_operations)
    return formatted_output
