install:
	poetry install

lint:
	poetry run black src tests
	poetry run mypy src

test:
	poetry run pytest tests/ -v

test-cov:
	poetry run pytest tests/ --cov=src/project_generator --cov-report=html --cov-report=term

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf dist/ build/ *.egg-info/ htmlcov/ .coverage

build:
	poetry build

run:
	poetry run pyfresh

.PHONY: install lint test test-cov clean build run
