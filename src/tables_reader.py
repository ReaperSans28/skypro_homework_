import pandas as pd


def csv_reader(file_path: str) -> list:
    """
    Функция возвращает содержимое файла с расширением .csv в виде словаря, если он существует.
    """
    try:
        data = pd.read_csv(file_path, sep=";")
        return data.to_dict("records")
    except FileNotFoundError:
        return []


def xlsx_reader(file_path: str) -> list:
    """
    Функция возвращает содержимое файла с расширением .xlsx или .xls в виде словаря, если он существует.
    """
    try:
        data = pd.read_excel(file_path)
        return data.to_dict("records")
    except FileNotFoundError:
        return []
