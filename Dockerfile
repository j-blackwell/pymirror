from python:3.10
copy --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV HOME=/opt/pymirror
ENV DAGSTER_HOME=/opt/pymirror/tmp
ENV LOCAL_DIR=/opt/pymirror/tmp/storage_assets
ENV SQLITE=/opt/pymirror/tmp/storage_assets/database.duckdb
RUN mkdir -p ${HOME}
RUN mkdir -p ${HOME}/tmp
RUN mkdir -p ${HOME}/tmp/storage_assets

COPY . ${HOME}
WORKDIR ${HOME}

run uv sync --frozen

expose 8000
