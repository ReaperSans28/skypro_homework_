import pytest

from src.masks import mask_account_number, mask_card_number


def mask_card_number_test() -> None:
    assert mask_card_number("Visa Platinum 7000792289606361") == "Visa Platinum 7000 79** **** 6361"
    assert mask_card_number("Maestro 1596837868705199") == "Maestro 1596 83** **** 5199"


@pytest.fixture
def test() -> str:
    return "**4305"


def test_with_fixture(test: str) -> None:
    assert test == mask_account_number("Счет 73654108430135874305")


def mask_account_number_test() -> None:
    assert mask_account_number("Счет 64686473678894779589") == "Счет **9589"
