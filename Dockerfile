FROM python:3.11-slim

WORKDIR /mini_backtesting_api

RUN apt-get update && apt-get install -y \
    curl gcc libpq-dev \
    && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY ./poetry.lock ./pyproject.toml /mini_backtesting_api/

RUN poetry install --no-interaction --no-root

RUN mkdir mini_backtesting_api

COPY ./app /mini_backtesting_api/app

COPY ./mini_backtesting_api.py /mini_backtesting_api

EXPOSE 8080

# CMD ["poetry", "run", "uvicorn", "mini_backtesting_api:app", "--host", "0.0.0.0", "--port", "8080",]
CMD poetry run uvicorn mini_backtesting_api:app --host 0.0.0.0 --port 8080
