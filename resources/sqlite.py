import sqlite3
import os
import pandas as pd
import datetime as dt
from typing import Callable

SQLITE = os.getenv("SQLITE")

class Sqlite():
    def __enter__(self):
        self.con = sqlite3.connect(SQLITE)
        return self.con
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.con.close()

def get_sql_widget_html(widget_name, con):
    cursor = con.cursor()
    cursor.execute("SELECT html_content FROM widgets WHERE widget_name=?", (widget_name,))
    widget = cursor.fetchone()
    try:
        return widget[0]
    except:
        return f"<div>No data for {widget_name} widget</div>"

def get_all_sql_widgets_html(widget_names):
    with Sqlite() as con:
        widgets = [get_sql_widget_html(w, con) for w in widget_names]
    return widgets

def update_sql_widget(widget_name: str, df: pd.DataFrame, fn: Callable, **kwargs) -> None:
    with Sqlite() as con:
        cursor = con.cursor()
        df.to_sql(widget_name, con=con, if_exists="replace")

        df_html = fn(df, **kwargs)
        updated_timestamp = dt.datetime.now()
        sql_update = """
        INSERT OR REPLACE INTO widgets (widget_name, html_content, updated)
        VALUES (?, ?, ?);
        """

        # Execute the update
        cursor.execute(sql_update, (widget_name, df_html, updated_timestamp))
        con.commit()
    return None

def instantiate():
    # Connect to SQLite database. If it doesn't exist, it will be created.
    with Sqlite() as con:

        # Create a new SQLite cursor.
        cursor = con.cursor()

        # Create `widgets` table.
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS widgets (
            widget_name TEXT PRIMARY KEY,
            html_content TEXT NOT NULL,
            updated TIMESTAMP NOT NULL
        )
        ''')

        # Commit the changes and close the connection.
        con.commit()

if __name__ == "__main__":
    instantiate()