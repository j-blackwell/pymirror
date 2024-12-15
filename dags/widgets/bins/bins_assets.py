import pandas as pd
import dagster as dg
from dags.resources.io_managers import HTML
from dags.resources.resources import SeleniumResource
from dags.widgets.bins.bins_transformations import get_bins_raw, transform_bins_data, transform_bins_html


@dg.asset
def bins_raw(selenium: SeleniumResource) -> pd.DataFrame:
    bins_raw = get_bins_raw(selenium._driver)
    return bins_raw

@dg.asset
def bins_data(bins_raw: pd.DataFrame) -> pd.DataFrame:
    bins_data = transform_bins_data(bins_raw)
    return bins_data

@dg.asset(io_manager_key="html_io_manager")
def bins_html(bins_data: pd.DataFrame) -> HTML:
    bins_html = transform_bins_html(bins_data)
    return bins_html
