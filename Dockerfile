from python:3.10
copy --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV HOME=/opt/pymirror
RUN mkdir -p ${HOME}
RUN mkdir -p ${HOME}/data

COPY . ${HOME}
WORKDIR ${HOME}

run uv sync --frozen
RUN uv run ./resources/sqlite.py

expose 8000
