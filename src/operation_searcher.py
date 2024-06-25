import re


def operation_finder(data: list, user_request: str) -> list:
    """
    Принимает список словарей с данными о банковских операциях и строку поиска.
    Возвращает список словарей, у которых в описании есть данная строка.
    """
    final_data = []
    for operation in data:
        if re.search(user_request, operation["description"]):
            final_data.append(operation)
    return final_data


def count_operation_by_category(data: list[dict], category: dict[str, list[str]]) -> dict[str, int]:
    """
    Принимает список словарей с данными о банковских операциях и словарь категорий операций.
    Возвращает словарь, в котором ключи — названия категорий, значения — количество операций в каждой категории.
    """
    count_operation: dict[str, int] = {}
    for item in data:
        for key, value in category.items():
            if item["description"] in value:
                count_operation[key] = count_operation.get(key, 0) + 1
    return count_operation
