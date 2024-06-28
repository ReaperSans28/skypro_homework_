import json
import os
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv

from src.logging import logging_setup

load_dotenv()

api = os.getenv("API_KEY")
logger = logging_setup()


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
        logger.info("Сработала get_financial_transactions")
        return transactions
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        logger.error("get_financial_transactions выдала ошибку")
        return []


def get_usd_value() -> Optional[float]:
    """Выдает актуальный курс доллара"""
    global api
    url = "https://open.er-api.com/v6/latest/USD"
    headers = {"apikey": api}
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200 and "rates" in data:
        if "USD" in data["rates"]:
            usd_rate = data["rates"]["USD"]
            logger.info("Сработала get_usd_value")
            return float(usd_rate)
    logger.error("get_usd_value не сработала")
    return None


def get_euro_value() -> Optional[float]:
    """Выдает актуальный курс евро"""
    global api
    url = "https://open.er-api.com/v6/latest/EUR"
    headers = {"apikey": api}
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200 and "rates" in data:
        if "EUR" in data["rates"]:
            euro_rate = data["rates"]["EUR"]
            logger.info("Сработала get_euro_value")
            return float(euro_rate)
    logger.error("get_euro_value не сработала")
    return None


def get_amount_transactions(transaction: dict) -> float:
    """
    Функция принимает на вход словарь с данными о финансовой транзакции и возвращает сумму транзакции
    в рублях.
    Иначе 0.0
    """
    global api
    amount_rub = 0.0

    if "operationAmount" in transaction:
        value = transaction["operationAmount"]
        currency = value.get("currency", {}).get("code", "")
        if currency == "USD":
            usd_value = get_usd_value()
            if usd_value is not None:
                amount_rub += float(value["amount"]) * usd_value
        elif currency == "EUR":
            euro_value = get_euro_value()
            if euro_value is not None:
                amount_rub += float(value["amount"]) * euro_value
        else:
            amount_rub += float(value["amount"])

    if amount_rub > 0:
        logger.info("Сработала get_amount_transactions")
        return amount_rub
    else:
        logger.error("get_amount_transactions выдала ошибку")
        return 0.0
