import dagster as dg
import pandas as pd
from dags.resources import resources

@dg.asset(io_manager_key="html_io_manager")
def test_asset() -> str:
    return ""

defs = dg.Definitions(
    assets=[test_asset],
    resources=resources,
    jobs=[],
    schedules=[],
    sensors=[],
)
