FROM python:3.12-slim

WORKDIR /app

# Install Poetry
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get remove -y curl && apt-get autoremove -y

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* /app/

# Install dependencies for bot group
RUN poetry config virtualenvs.create false && \
    poetry install --only main,bot --no-interaction --no-ansi

# Copy the rest of the application
COPY . .

CMD ["python", "bot.py"]