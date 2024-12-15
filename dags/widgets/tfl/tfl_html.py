import pandas as pd
import datetime as dt

from dags.resources.io_managers import HTML


def departures_html(df: pd.DataFrame) -> HTML:
    df_sorted = (
        df.loc[
            lambda df: pd.to_datetime(df["expectedArrival"])
            > pd.Timestamp("now", tz="UTC")
        ]
        .assign(
            expectedArrivalLocal=lambda df: pd.to_datetime(df["expectedArrivalLocal"])
        )
        .sort_values(["lineName", "expectedArrivalLocal"])
    )

    if df_sorted.shape[0] == 0:
        return HTML("<h4>No departures</h4>")

    df_grouped = df_sorted.groupby(["lineName"])

    dfs = {x: df_grouped.get_group(x) for x in df_grouped.groups}
    html_all = ""
    for line, departures in dfs.items():
        html = f"\n<h4>{departures.iloc[0]['stationName']} ({line})</h4>\n<ol>"
        for idx, row in departures.iterrows():
            html += f"\n<li>{row['destinationName']} - {row['expectedArrivalLocal'].strftime('%H:%M')}</li>"
        html += "\n<ol>"

        html_all += html

    return HTML(html_all)


def status_html(df: pd.DataFrame) -> HTML:
    html_all = "<h3>Status</h3>\n<ul>"
    for idx, row in df.iterrows():
        html_all += f"\n<li>{row['line']} - {row['status']}"

        if row["status"] == "Good Service":
            html_all += "</li>"
        else:
            # html_all += f"""<ul>
            #     <li>{row['disruption']} ({row['validity_from']} - {row['validity_to']})</li>
            #     <li>{row['reason']}</li>
            # </ul>"""
            html_all += "</li>"

    return HTML(html_all)
