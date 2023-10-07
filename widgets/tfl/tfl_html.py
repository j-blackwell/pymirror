import pandas as pd

def departures_html(df: pd.DataFrame) -> str:
    df_sorted = (
        df
        .sort_values(["lineName", "expectedArrivalLocal"])
        .groupby(["lineName"])
    )

    dfs = {x: df_sorted.get_group(x) for x in df_sorted.groups}
    html_all = ""
    for line, departures in dfs.items():
        html = f"\n<h4>{departures.iloc[0]['stationName']} ({line})</h4>\n<ol>"
        for idx, row in departures.iterrows():
            html += f"\n<li>{row['destinationName']} - {row['expectedArrivalLocal'].strftime('%H:%M')}</li>"
        html += "\n<ol>"

        html_all += html

    return html_all


def status_html(df: pd.DataFrame) -> str:
    html_all = "<h3>Status</h3>\n<ul>"
    for idx, row in df.iterrows():
        html_all += f"\n<li>{row['line']} - {row['status']}"

        if row['status'] == "Good Service":
            html_all += "</li>"
        else:
            # html_all += f"""<ul>
            #     <li>{row['disruption']} ({row['validity_from']} - {row['validity_to']})</li>
            #     <li>{row['reason']}</li>
            # </ul>"""
            html_all += "</li>"

    return html_all
