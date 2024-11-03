from python:3.10
copy --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

copy . .

run uv sync --frozen

expose 8000
