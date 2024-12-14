import json
from pathlib import Path
from typing import Any, Optional, Sequence, Type, Union
import dagster as dg
from dagster._core.storage.db_io_manager import DbIOManager, DbTypeHandler
from dagster_duckdb.io_manager import DuckDbClient
from dagster_duckdb import DuckDBIOManager


class HTML(str):
    pass

def build_custom_duckdb_io_manager(
    type_handlers: Sequence[DbTypeHandler],
    default_load_type: Optional[Type] = None,
) -> dg.IOManagerDefinition:
    @dg.io_manager(config_schema=DuckDBIOManager.to_config_schema())
    def duckdb_io_manager(init_context):
        return DbIOManager(
            type_handlers=type_handlers,
            db_client=DuckDbClient(),
            database=init_context.resource_config["database"],
            schema=init_context.resource_config.get("schema"),
            default_load_type=default_load_type,
        )

    return duckdb_io_manager

class LocalHtmlIOManager(dg.UPathIOManager):
    extension: Optional[str] = ".html"

    def __init__(self, base_dir: str):
        self._base_dir = base_dir
        self._base_path = Path(base_dir)


    def _metadata(self, context: Union[dg.InputContext, dg.OutputContext]) -> dict:
        try:
            metadata = context.upstream_output.metadata
        except AttributeError:
            metadata = context.definition_metadata

        return metadata

    def dump_to_path(self, context, obj: Any, path: Path):
        self.make_directory(path.parent)

        context.log.debug(f"Writing content to {path}")
        with open(path, "w") as f:
            f.write(obj)

        context.add_output_metadata(
            {
                "path": dg.PathMetadataValue(path),
                "preview": dg.MarkdownMetadataValue(obj),
            }
        )

    def load_from_path(self, context: dg.InputContext, path: Path):
        context.log.debug(f"Reading content from {path}")
        with open(path, "r") as f:
            obj = f.read()

        return obj

    def load_input(self, context: dg.InputContext) -> Any:
        path = self._get_path(context)
        return self.load_from_path(context, path)

    def handle_output(self, context: dg.OutputContext, obj: Any) -> None:
        path = self._get_path(context)
        self.dump_to_path(context, obj, path)


@dg.io_manager(
    config_schema={
        "base_dir": dg.Field(dg.StringSource),
    },
)
def local_html_io_manager(init_context):
    return LocalHtmlIOManager(init_context.resource_config["base_dir"])

class LocalJsonIOManager(LocalHtmlIOManager):
    extension: Optional[str] = ".json"

    def dump_to_path(self, context, obj: Any, path: Path):
        self.make_directory(path.parent)

        context.log.debug(f"Writing content to {path}")
        with open(path, "w") as f:
            json.dump(obj, f)

        context.add_output_metadata(
            {
                "path": dg.PathMetadataValue(path),
            }
        )

    def load_from_path(self, context: dg.InputContext, path: Path):
        context.log.debug(f"Reading content from {path}")
        with open(path, "r") as f:
            obj = json.load(f)

        return obj


@dg.io_manager(
    config_schema={
        "base_dir": dg.Field(dg.StringSource),
    },
)
def local_json_io_manager(init_context):
    return LocalJsonIOManager(init_context.resource_config["base_dir"])

