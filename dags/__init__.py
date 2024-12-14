import dagster as dg

from dags.resources.definitions import resources
from dags.widgets.bins import bins_assets
from dags.widgets.football import football_assets
from dags.widgets.tfl import tfl_assets
from dags.widgets.weather import weather_assets

assets = dg.load_assets_from_modules(
    [
        bins_assets,
        football_assets,
        tfl_assets,
        weather_assets,
    ]
)


defs = dg.Definitions(
    assets=assets,
    resources=resources,
    jobs=[],
    schedules=[],
    sensors=[],
)
