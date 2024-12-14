import pandas as pd
from dagster_duckdb_pandas.duckdb_pandas_type_handler import DuckDBPandasTypeHandler
from dagster_duckdb_polars.duckdb_polars_type_handler import DuckDBPolarsTypeHandler

from dags.resources.io_managers import build_custom_duckdb_io_manager, local_html_io_manager, local_json_io_manager
from dags.resources.resources import SeleniumResource

resources = {
    "io_manager": build_custom_duckdb_io_manager(
        type_handlers=[
            DuckDBPandasTypeHandler(),
            DuckDBPolarsTypeHandler(),
        ],
        default_load_type=pd.DataFrame,
    ).configured({"database": {"env": "SQLITE"}}),
    "html_io_manager": local_html_io_manager.configured({"base_dir": {"env": "LOCAL_DIR"}}),
    "json_io_manager": local_json_io_manager.configured({"base_dir": {"env": "LOCAL_DIR"}}),
    "selenium": SeleniumResource(),
}
