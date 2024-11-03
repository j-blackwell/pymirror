import duckdb
import os
import pandas as pd
import datetime as dt
from typing import Callable
from contextlib import contextmanager
from dotenv import dotenv_values


@contextmanager
def get_db_con():
    env = dotenv_values()
    with duckdb.connect(database=env["SQLITE"]) as con:
        yield con


def get_sql_widget_html(widget_name):
    with get_db_con() as con:
        cursor = con.cursor()
        cursor.execute(
            "SELECT html_content FROM widgets WHERE widget_name=?", (widget_name,)
        )
        widget = cursor.fetchone()

    try:
        return widget[0]
    except (IndexError, TypeError):
        return f"<div>No data for {widget_name} widget</div>"


def get_all_sql_widgets_html(widget_names):
    widgets = [get_sql_widget_html(w) for w in widget_names]
    return widgets


def update_sql_html(widget_name, html) -> None:
    updated_timestamp = dt.datetime.now()
    sql_update = """
    INSERT OR REPLACE INTO widgets (widget_name, html_content, updated)
    VALUES (?, ?, ?);
    """

    with get_db_con() as con:
        cursor = con.cursor()
        cursor.execute(sql_update, (widget_name, html, updated_timestamp))
        con.commit()


def update_sql_df(widget_name: str, df: pd.DataFrame):
    with get_db_con() as con:
        df.to_sql(widget_name, con=con, if_exists="replace", index=False)


def update_sql_widget(
    widget_name: str, df: pd.DataFrame, fn: Callable, **kwargs
) -> None:
    update_sql_df(widget_name, df)
    df_html = fn(df, **kwargs)
    update_sql_html(widget_name, df_html)
    return None


def instantiate():
    # Connect to SQLite database. If it doesn't exist, it will be created.
    with get_db_con() as con:
        # Create a new SQLite cursor.
        cursor = con.cursor()

        # Create `widgets` table.
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS widgets (
            widget_name TEXT PRIMARY KEY,
            html_content TEXT NOT NULL,
            updated TIMESTAMP NOT NULL
        )
        """
        )

        # Commit the changes and close the connection.
        con.commit()


if __name__ == "__main__":
    instantiate()
