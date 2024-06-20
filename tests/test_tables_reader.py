from unittest.mock import patch
import pandas as pd
from src.tables_reader import csv_reader, xlsx_reader


def test_csv_reader() -> None:
    with patch("pandas.read_csv") as mock_csv:
        mock_csv.return_value = pd.DataFrame({"Date": ["2023-07-11", "2017-12-02"], "Amount": [50.00, 1.00]})
        data = csv_reader("data/transactions.csv")
        assert data == [{"Date": "2023-07-11", "Amount": 50.00}, {"Date": "2017-12-02", "Amount": 1.00}]


def test_excel_reader() -> None:
    with patch("pandas.read_excel") as mock_excel:
        mock_excel.return_value = pd.DataFrame({"Date": ["2023-07-11", "2017-12-02"], "Amount": [50.00, 1.00]})
        data = xlsx_reader("data/transactions.excel.xlsx")
        assert data == [{"Date": "2023-07-11", "Amount": 50.00}, {"Date": "2017-12-02", "Amount": 1.00}]


def test_wrong_path() -> None:
    excel_data = xlsx_reader("test.xls")
    csv_data = csv_reader("test.csv")
    assert excel_data == []
    assert csv_data == []
