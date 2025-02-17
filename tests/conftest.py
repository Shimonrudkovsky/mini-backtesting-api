import pytest
import sys
import os
import pandas as pd
import numpy as np
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
