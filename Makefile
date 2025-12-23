.PHONY: install install-dev test run docker-build docker-run clean lint format

# Install production dependencies
install:
	poetry install --no-dev --no-root

# Install all dependencies including dev
install-dev:
	poetry install --no-root --with dev

# Run tests with coverage
test:
	poetry run pytest

# Run Flask development server
run:
	poetry run flask run

# Build Docker image
docker-build:
	docker build -t ask:latest .

# Run Docker container (requires OPENAI_API_KEY)
docker-run:
	docker run -p 5000:5000 -e OPENAI_API_KEY=${OPENAI_API_KEY} ask:latest

# Clean up generated files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

# Help command
help:
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make install-dev   - Install all dependencies including dev"
	@echo "  make test          - Run tests with coverage"
	@echo "  make run           - Run Flask development server"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"
	@echo "  make clean         - Clean up generated files"
