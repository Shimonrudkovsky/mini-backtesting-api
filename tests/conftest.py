import os
import sys

import numpy as np
import pandas as pd
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.routes.backtest import router
from mini_backtesting_api import validation_exception_handler

# Add parent directory to the sys.path to resolve relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope='module')
def test_app():
    app = FastAPI()
    app.include_router(router)
    app.add_exception_handler(Exception, validation_exception_handler)
    return app


@pytest.fixture(scope='module')
def client(test_app):
    return TestClient(test_app)


@pytest.fixture(scope="module")
def df():
    securities = [str(i) for i in range(1000)]
    dates = pd.date_range("2020-01-01", "2025-01-22")

    data = np.random.uniform(low=1, high=100, size=(len(dates), len(securities)))
    data_frame = pd.DataFrame(
        data,
        index=dates,
        columns=securities,
    )

    return data_frame


@pytest.fixture(scope="module")
def mini_df():
    data_frame = pd.DataFrame(
        data=[
            [0.4, 0.1, 0.7, 0.2, 0.9, 0.22, 0.99],
            [0.7, 0.1, 0.5, 0.4, 0.3, 0.2, 0.1],
            [0.11, 0.22, 0.33, 0.44, 0.55, 0.66, 0.77],
        ],
        index=["2021-01-17", "2022-02-27", "2023-03-29"],
        columns=["1", "2", "3", "4", "5", "6", "7"],
    )

    return data_frame


@pytest.fixture(scope="module")
def filtered_df():
    data_frame = pd.DataFrame(
        data=[
            [4.4, 7.7, None, 9.9, 22.22, 99.99],
            [7.7, 5.5, 2.4, None, 2.2, None],
            [None, 33.33, 44.44, 1.55, 22.66, 9.77],
        ],
        index=["2021-01-17", "2022-02-27", "2023-03-29"],
        columns=["1", "3", "4", "5", "6", "7"],
    )

    return data_frame
