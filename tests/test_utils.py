from unittest.mock import Mock, patch

import pytest
import requests
from dotenv import load_dotenv

from src.utils import get_financial_transactions, get_euro_value, get_usd_value, get_amount_transactions

path = "C:\\Users\\student\\PycharmProjects\\skypro_homework1828\\data\\data.json"

load_dotenv()

file_path_wrong = ""


@pytest.fixture
def operation18() -> list:
    # 18 operation, because 28
    return [
        {
            "id": 782295999,
            "state": "EXECUTED",
            "date": "2019-09-11T17:30:34.445824",
            "operationAmount": {"amount": "54280.01", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Счет 24763316288121894080",
            "to": "Счет 96291777776753236930",
        }
    ]


def test_get_financial_transactions() -> None:
    mock_test = Mock(return_value=[])
    assert get_financial_transactions(file_path_wrong) == mock_test()
    assert type(get_financial_transactions(path)) == list


def test_get_amount_transactions() -> None:
    mock_test = Mock(return_value=0.0)
    assert get_amount_transactions([]) == mock_test()


def test_get_euro_value() -> None:
    assert type(get_euro_value()) is not None


def test_get_usd_value() -> None:
    assert type(get_usd_value()) is not None


def test_get() -> None:
    url1 = "https://www.cbr-xml-daily.ru/daily_json.js"
    response1 = requests.get(url1)
    assert response1.status_code == 200


def test_transaction_sum(operation18: list) -> None:
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = operation18
        assert get_amount_transactions(operation18) == 54280.01
