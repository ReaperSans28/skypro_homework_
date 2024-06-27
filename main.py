import re
from src.tables_reader import csv_reader, xlsx_reader
from src.generators import filter_by_currency, transaction_descriptions
from src.operation_searcher import operation_finder
from src.processing import filter_state, sort_by_date
from src.utils import get_financial_transactions, get_amount_transactions
from src.widget import number_or_account


def main_fail():
    """Выводит ошибку, если что-то пошло не так"""
    return "Такой тип операции не поддерживается. Попробуйте ещё раз.\n"


def file_format():
    """
    Определяет расширение файла, с которым будем работать.
    """
    print("Добрый день, вы попали в программу для работы с банковскими транзакциями.")
    file = input(
        """Выберите номер формата файла:
    1. .json
    2. .csv
    3. .xlsx или .xls\n"""
    )
    if file == "1":
        print("Для работы выбран файл с расширением .json.\n")
        return get_financial_transactions("data/data.json"), "json"
    if file == "2":
        print("Для работы выбран файл с расширением .csv.\n")
        return csv_reader("data/transactions.csv"), "csv"
    if file == "3":
        print("Для работы выбран excel файл.\n")
        return xlsx_reader("data/transactions_excel.xlsx"), "excel"
    else:
        print(main_fail())
        file_format()
        return [], ""


def status_sort(data):
    """Сортировка по статусу операции в виде консольного приложения"""
    print("Выберите статус, по которому необходимо выполнить фильтрацию.")
    status = input("Доступные для сортировки статусы: EXECUTED, CANCELED, PENDING\n")

    if status.upper() not in ("EXECUTED", "CANCELED", "PENDING"):
        print(main_fail())
        status_sort(data)
    return filter_state(data, status)


def date_sort(data):
    """Сортировка по дате в виде консольного приложения"""
    to_sort = input("Отсортировать операции по дате? Да/Нет \n")
    if to_sort.lower() == "да":
        time = input("По возрастанию(1) или по убыванию(2)?\n")
        if time.lower() == "1":
            return sort_by_date(data)
        elif time.lower() == "2":
            return sort_by_date(data, "decreasing")
        else:
            print(main_fail())
            date_sort(data)
            return []
    elif to_sort.lower() == "нет":
        return data
    else:
        print(main_fail())
        date_sort(data)
        return []


def only_rub(data, file_type):
    """Сортировка по валюте в виде консольного приложения"""
    to_sort = input("Выводить только рублевые транзакции? Да/Нет \n")
    if to_sort.lower() == "да":
        sorted_data = []
        for item in filter_by_currency(data, "RUB"):
            sorted_data.append(item)
        return sorted_data
    elif to_sort.lower() == "нет":
        return data
    else:
        print(main_fail())
        only_rub(data, file_type)
        return []


def word_sort(data):
    """Сортировка по ключевым словам в описании в виде консольного приложения"""
    to_sort = input("Отфильтровать список операций по определённому слову в описании? Да/Нет\n")
    if to_sort.lower() == "да":
        to_find = input("Что вы хотели бы найти? \n")
        return operation_finder(data, to_find)
    elif to_sort.lower() == "нет":
        return data
    else:
        print(main_fail())
        word_sort(data)
        return []


def main() -> None:
    """Основная функция, содержащая все остальные"""
    # Определение файла, с которым пользователь хотел бы работать в формате консольного приложения
    data, file_type = file_format()
    data = status_sort(data)
    data = date_sort(data)
    data = only_rub(data, file_type)
    data = word_sort(data)

    print("Распечатываю список транзакций...")
    if data and len(data) != 0:
        print(f"Всего операций в выборке: {len(data)}\n")
        for operation in data:
            print(
                operation["date"],
                next(transaction_descriptions(data)),
            )
            if re.search("Перевод", operation["description"]):
                print(number_or_account(operation["from"]), " -> ", number_or_account(operation["to"]))
            else:
                print(number_or_account(operation["to"]))
            # Передаем одну транзакцию (operation) в функцию
            print(f"Сумма: {get_amount_transactions(operation)}руб. \n")
    else:
        print("Не найдено ни одной транзакции подходящей под ваши условия фильтрации")


if __name__ == "__main__":
    main()
