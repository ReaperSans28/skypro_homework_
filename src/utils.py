import json
import os
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

api = os.getenv("API_KEY")


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


def get_usd_value(api_key: str) -> Optional[float]:
    url = "https://open.er-api.com/v6/latest/USD"
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200 and "conversion_rates" in data:
        if "RUB" in data["conversion_rates"]:
            usd_rate = data["conversion_rates"]["RUB"]
            return float(usd_rate)
    return None


def get_euro_value(api_key: str) -> Optional[float]:
    url = "https://open.er-api.com/v6/latest/EUR"
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200 and "conversion_rates" in data:
        if "RUB" in data["conversion_rates"]:
            euro_rate = data["conversion_rates"]["RUB"]
            return float(euro_rate)
    return None


def get_amount_transactions(request: str, api_key: str) -> float:
    try:
        with open(request, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return 0.0

        amount_rub = 0.0
        for item in data:
            if "operationAmount" in item:
                value = item["operationAmount"]
                currency = value.get("currency", {}).get("code", "")
                if currency == "USD":
                    usd_value = get_usd_value(api_key)
                    if usd_value is not None:
                        amount_rub += float(value["amount"]) * usd_value
                elif currency == "EUR":
                    euro_value = get_euro_value(api_key)
                    if euro_value is not None:
                        amount_rub += float(value["amount"]) * euro_value
                else:
                    amount_rub += float(value["amount"])

        return amount_rub

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return 0.0


path = "C:\\Users\\student\\PycharmProjects\\skypro_homework1828\\data\\data.json"
converted_amount = get_amount_transactions(path, api)
print(f"Converted amount in rubles: {converted_amount}")
