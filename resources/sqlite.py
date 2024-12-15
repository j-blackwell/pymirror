import dagster as dg
from importlib import import_module


def get_sql_widget_html(asset_key: dg.AssetKey):
    dags = import_module("dags")
    defs : dg.Definitions = dags.defs

    try:
        return defs.load_asset_value(asset_key)
    except FileNotFoundError:
        return f"<div>No data for {asset_key.path[-1]} widget</div>"


def get_all_sql_widgets_html(widget_names):
    widgets = [get_sql_widget_html(w) for w in widget_names]
    return widgets
