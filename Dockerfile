FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -qq -y --no-install-recommends \
	build-essential \
	curl \
	 && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-interaction --no-ansi

COPY . /app/

EXPOSE 8080

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]