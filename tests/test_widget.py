import pytest

from src.widget import convert_date_, number_or_account


def convert_date_test_() -> None:
    assert convert_date_("2018-07-11T02:26:18.671407") == "11.07.2018"


@pytest.fixture
def test() -> str:
    return "Счет **4305"


def test_with_fixture(test: str) -> None:
    assert test == number_or_account("Счет 73654108430135874305")
