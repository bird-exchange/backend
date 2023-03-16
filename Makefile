-include .env
export

app.run:
	@python -m backend

db.run:
	@docker-compose up -d db

minio.run:
	@docker-compose up -d minio

test:
	@python -m pytest -x tests/

test.coverage:
	@coverage run -m pytest
	@coverage report
