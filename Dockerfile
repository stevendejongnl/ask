FROM python:3.12-slim

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files first for better caching
COPY pyproject.toml poetry.lock ./

# Install dependencies (production only)
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --only main

# Copy application code
COPY . .

# Set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run Flask application
CMD ["poetry", "run", "flask", "run"]