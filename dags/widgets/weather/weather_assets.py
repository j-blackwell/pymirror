import dagster as dg
import pandas as pd

from dags.resources.io_managers import HTML
from dags.widgets.weather.weather_html import (
    transform_weather_current_html,
    transform_weather_daily_html,
)
from dags.widgets.weather.weather_transformations import (
    get_weather_raw,
    transform_weather_current,
    transform_weather_daily,
)


@dg.asset(io_manager_key="json_io_manager")
def weather_raw() -> dict:
    return get_weather_raw()

@dg.asset
def weather_daily(weather_raw: dict) -> pd.DataFrame:
    return transform_weather_daily(weather_raw)

@dg.asset
def weather_current(weather_raw: dict) -> pd.DataFrame:
    return transform_weather_current(weather_raw)

@dg.asset(io_manager_key="html_io_manager")
def weather_daily_html(weather_daily: pd.DataFrame) -> HTML:
    return transform_weather_daily_html(weather_daily)

@dg.asset(io_manager_key="html_io_manager")
def weather_current_html(weather_current: pd.DataFrame) -> HTML:
    return transform_weather_current_html(weather_current)
