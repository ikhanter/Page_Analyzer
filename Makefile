install:
	poetry install

dev:
	poetry run flask --app page_analyzer.page_analyzer:app run --debug

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer.page_analyzer:app

lint:
	poetry run ruff check .

build:
	./build.sh

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml