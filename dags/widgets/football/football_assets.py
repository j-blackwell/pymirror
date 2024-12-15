import re

import dagster as dg
import pandas as pd

from dags.resources.io_managers import HTML
from dags.widgets.football.football_transformations import (
    get_football_matches,
    transform_football_latest_result_html,
    transform_football_matches,
    transform_football_next_fixture_html,
    transform_football_result_comparison_html,
)


@dg.multi_asset(
    outs={
        "football_matches": dg.AssetOut(),
        "football_matches_prev": dg.AssetOut(),
    },
    # automation_condition=dg.AutomationCondition.on_cron("@daily"),
)
def football_matches_raw():
    return get_football_matches()


@dg.multi_asset(
    outs={
        "football_latest_result": dg.AssetOut(),
        "football_next_fixture": dg.AssetOut(),
        "football_result_comparison": dg.AssetOut(),
    },
    # automation_condition=dg.AutomationCondition.eager(),
)
def football_matches_curated(
    football_matches: pd.DataFrame,
    football_matches_prev: pd.DataFrame,
):
    return transform_football_matches(football_matches, football_matches_prev)


@dg.asset(
    io_manager_key="html_io_manager",
    automation_condition=dg.AutomationCondition.eager(),
)
def football_latest_result_html(football_latest_result: pd.DataFrame) -> HTML:
    return transform_football_latest_result_html(football_latest_result)


@dg.asset(
    io_manager_key="html_io_manager",
    automation_condition=dg.AutomationCondition.eager(),
)
def football_next_fixture_html(football_next_fixture):
    return transform_football_next_fixture_html(football_next_fixture)


@dg.asset(
    io_manager_key="html_io_manager",
    automation_condition=dg.AutomationCondition.eager(),
)
def football_result_comparison_html(football_result_comparison):
    return transform_football_result_comparison_html(football_result_comparison)
