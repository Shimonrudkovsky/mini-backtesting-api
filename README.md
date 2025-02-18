# Mini Backtesting API

This project provides a FastAPI-based API for running backtests on historical data. The API includes endpoints for submitting backtest requests and handling various constraints and errors.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/mini-backtesting-api.git
    cd mini-backtesting-api
    ```

## Running the API

### Using Docker Compose

1. Build and start the containers:

    ```sh
    docker-compose up --d
    ```

2. The API will be available at `localhost:80`.

### Using Uvicorn

To start the FastAPI server without Docker, run:

```sh
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:80.

## Endpoints
/backtest
#### Method: POST
#### Summary: Runs backtest on historical data.
#### Request Body:

```json
{
    "dataset": "market_capitalization",
    "calendar_rule": {
        "type": "quarterly",
        "initial_date": "2021-01-17"
    },
    "portfolio_filter": {
        "type": "top_n",
        "top": 5
    },
    "weighting_method": {
        "type": "optimized",
        "lower_bound": 0.15,
        "upper_bound": 0.6
    }
}
```