import json
from typing import Dict, List, Optional

import requests


def get_financial_transactions(request: str) -> List[Dict]:
    """
    Функция принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях.
    Иначе пустой список.
    """
    try:
        with open(request, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        transactions = []
        for item in data:
            if "operationAmount" in item and isinstance(item["operationAmount"], dict):
                if "amount" in item["operationAmount"]:
                    transactions.append(item)
        return transactions
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []


def get_usd_value() -> Optional[float]:
    """Функция выдает актуальный курс доллара, если он доступен."""
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        usd_rate = data["Valute"]["USD"]["Value"]
        return float(usd_rate)
    else:
        return None


def get_euro_value() -> Optional[float]:
    """Функция выдает актуальный курс евро, если он доступен."""
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        euro_rate = data["Valute"]["EUR"]["Value"]
        return float(euro_rate)
    else:
        return None


def get_amount_transactions(request: str) -> List[float]:
    """
    Принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях, возвращает тип float.
    Если транзакция была в USD или EUR, идет обращение к функциям, которые дадут актуальный курс валюты и
    происходит конвертация сумм.
    """
    try:
        with open(request, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return [0.0]

        amount = []
        for item in data:
            if "operationAmount" in item:
                amount.append(item["operationAmount"])

        amount_rub = []
        for value in amount:
            if value["currency"] == {"name": "USD", "code": "USD"}:
                usd_value = get_usd_value()
                if usd_value is not None:
                    amount_rub.append(float(value["amount"]) * usd_value)
            elif value["currency"] == {"name": "EUR", "code": "EUR"}:
                euro_value = get_euro_value()
                if euro_value is not None:
                    amount_rub.append(float(value["amount"]) * euro_value)
            else:
                amount_rub.append(float(value["amount"]))

        return amount_rub

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return [0.0]
