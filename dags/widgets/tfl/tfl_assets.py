import dagster as dg
import pandas as pd

from dags.resources.io_managers import HTML
from dags.widgets.tfl.tfl_departures import get_tfl_departures_raw, transform_tfl_departures
from dags.widgets.tfl.tfl_html import departures_html, status_html
from dags.widgets.tfl.tfl_status import get_tfl_status_raw, transform_tfl_status


@dg.asset(io_manager_key="json_io_manager")
def tfl_departures_raw() -> list:
    return get_tfl_departures_raw()


@dg.asset(io_manager_key="json_io_manager")
def tfl_status_raw() -> list:
    return get_tfl_status_raw()


@dg.asset
def tfl_departures(tfl_departures_raw: list) -> pd.DataFrame:
    return transform_tfl_departures(tfl_departures_raw)


@dg.asset
def tfl_status(tfl_status_raw: list) -> pd.DataFrame:
    return transform_tfl_status(tfl_status_raw)


@dg.asset(io_manager_key="html_io_manager")
def tfl_departures_html(tfl_departures: pd.DataFrame) -> HTML:
    return departures_html(tfl_departures)


@dg.asset(io_manager_key="html_io_manager")
def tfl_status_html(tfl_status: pd.DataFrame) -> HTML:
    return status_html(tfl_status)
