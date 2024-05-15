from unittest.mock import Mock

import requests

from src.utils import get_amount_transactions, get_euro_value, get_financial_transactions, get_usd_value

file_path_wrong = ""


def test_get_financial_transactions() -> None:
    mock_test = Mock(return_value=[])
    assert get_financial_transactions(file_path_wrong) == mock_test()


def test_get_amount_transactions() -> None:
    mock_test = Mock(return_value=[0.0])
    assert get_amount_transactions(file_path_wrong) == mock_test()


def test_get_euro_value() -> None:
    assert type(get_euro_value()) is float


def test_get_usd_value() -> None:
    assert type(get_usd_value()) is float


def test_get() -> None:
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)
    assert response.status_code == 200
