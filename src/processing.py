from typing import Dict, List, Tuple


def filter_state(data: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Функция принимает список словарей и значение для ключа state (по умолчанию EXECUTED)
    возвращает список, содержащий только словари, у которых значение ключа state совпадает с переданным в функцию.
    """
    filtered_list = []
    for d in data:
        if d.get("state") == state:
            filtered_list.append(d)
    return filtered_list


def convert_date(date: str) -> Tuple[int, int, int, int, int, int]:
    """
    Функция раскидывает каждое значение даты в отдельную переменную.
    """
    year = int(date[:4])
    month = int(date[5:7])
    day = int(date[8:10])
    hour = int(date[11:13])
    minute = int(date[14:16])
    second = int(date[17:19])
    return year, month, day, hour, minute, second


def key_for_sort(x: Dict) -> Tuple[int, int, int, int, int, int]:
    """Функция выдает ключ для работы функции sort_by_date."""
    return convert_date(x["date"])


def sort_by_date(data: List[Dict], order: str = "desc") -> List[Dict]:
    """
    Сортирует по времени.
    """
    reverse = order.lower() == "desc"
    return sorted(data, key=key_for_sort, reverse=reverse)
