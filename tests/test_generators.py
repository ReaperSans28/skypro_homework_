from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return transactions


@pytest.mark.parametrize("value_type, expected_count", [("USD", 3), ("RUB", 2), ("EUR", 0)])
def test_filter_by_currency(sample_transactions: List[Dict[str, Any]], value_type: str, expected_count: int) -> None:
    filtered_transactions = list(filter_by_currency(sample_transactions, value_type))
    assert len(filtered_transactions) == expected_count


def test_transaction_descriptions(sample_transactions: List[Dict[str, Any]]) -> None:
    descriptions = list(transaction_descriptions(sample_transactions))
    assert len(descriptions) == 5
    assert "Перевод с карты на карту" in descriptions
    assert "Перевод со счета на счет" in descriptions
    assert "Перевод организации" in descriptions


@pytest.mark.parametrize(
    "first_numb, second_numb, expected_count",
    [(1111111111111111, 1111111111111113, 3), (2222222222222222, 2222222222222225, 4)],
)
def test_card_number_generator(first_numb: int, second_numb: int, expected_count: int) -> None:
    generated_cards = list(card_number_generator(first_numb, second_numb))
    assert len(generated_cards) == expected_count
