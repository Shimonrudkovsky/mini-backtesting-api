from unittest.mock import patch

import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from botocore.exceptions import DataNotFoundError


@pytest.fixture
def mock_parquet_data(df):
    table = pa.Table.from_pandas(df)
    parquet_bytes = pa.BufferOutputStream()
    pq.write_table(table, parquet_bytes)
    return parquet_bytes.getvalue()


def test_backtest_valid_request(client, mock_parquet_data):
    valid_request = {
        "dataset": "market_capitalization",
        "calendar_rule": {
            "type": "quarterly",
            "initial_date": "2021-01-17",
        },
        "portfolio_filter": {
            "type": "top_n",
            "top": 10,
        },
        "weighting_method": {
            "type": "equal",
        },
    }

    with patch('app.adapters.s3_client.get_from_s3', return_value=mock_parquet_data):
        response = client.post("/backtest", json=valid_request)
        assert response.status_code == 200


def test_backtest_data_not_found(client, mock_parquet_data):
    valid_request = {
        "dataset": "market_capitalization",
        "calendar_rule": {
            "type": "quarterly",
            "initial_date": "2021-01-17",
        },
        "portfolio_filter": {
            "type": "top_n",
            "top": 10,
        },
        "weighting_method": {
            "type": "equal",
        },
    }

    with patch("app.adapters.s3_client.get_from_s3", side_effect=DataNotFoundError(data_path="market_capitalization")):
        response = client.post("/backtest", json=valid_request)
        assert response.status_code == 400
        assert response.text == '{"detail":"No data was found"}'


def test_backtest_invalid_request(client):
    invalid_request = {
        "dataset": "abc",
        "calendar_rule": {
            "type": "quarterly",
            "initial_date": "2021-01-17",
        },
        "portfolio_filter": {
            "type": "top_n",
            "top": 10,
        },
        "weighting_method": {
            "type": "equal",
        },
    }
    response = client.post("/backtest", json=invalid_request)
    assert response.status_code == 422
