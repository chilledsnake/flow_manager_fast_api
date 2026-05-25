.PHONY: run test test-unit test-integration test-e2e lint format

run:
	uvicorn app.main:app --reload

test:
	pytest -v

test-unit:
	pytest -v tests/unit/

test-integration:
	pytest -v tests/integration/

test-e2e:
	pytest -v tests/e2e/

lint:
	ruff check .

format:
	ruff format .