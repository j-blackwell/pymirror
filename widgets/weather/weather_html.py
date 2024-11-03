import pandas as pd


def weather_current_html(df: pd.DataFrame) -> str:
    html_all = "<h3>Current Weather</h3>\n<ul>"
    for idx, row in df.iterrows():
        html_all += f"\n<li>Weather - {row['weather_main']}</li>"
        html_all += f"\n<li>Temp - {row['feels_like']:.0f}°C</li>"
        html_all += f"\n<li>Rain - {row['rain_prob']*100:.2f}%</li>"
        html_all += f"\n<li>UV - {row['uv_index']}</li>"

    html_all += "</ul>"

    return html_all


def weather_daily_html(df: pd.DataFrame) -> str:
    ...
