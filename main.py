from utils import load_json, get_last_executed_operations

FILENAME = "operations.json"


def main():
    """Основная функция программы"""
    operations_data = load_json(FILENAME)

    num_operations_to_display = 5
    last_executed_operations = get_last_executed_operations(operations_data, num_operations=num_operations_to_display)
    print(last_executed_operations)


if __name__ == "__main__":
    main()
