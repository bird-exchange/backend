-include .env
export

dev.install:
	@poetry install


lint:
	@mypy backend
	@flake8 backend

test:
	@python -m pytest tests/
