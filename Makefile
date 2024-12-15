local:
	uv run uvicorn app.main:app --reload

daemon:
	uv run dagster daemon
