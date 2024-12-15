from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from app.datetime_widget import get_datetime_widget
from dags.widgets.bins.bins_assets import bins_html
from dags.widgets.football.football_assets import (
    football_latest_result_html,
    football_next_fixture_html,
    football_result_comparison_html,
)
from dags.widgets.tfl.tfl_assets import tfl_departures_html, tfl_status_html
from dags.widgets.weather.weather_assets import weather_current_html, weather_daily_html
from resources.sqlite import get_all_sql_widgets_html

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def home(request: Request):
    datetime_widget = get_datetime_widget()
    right_widgets = get_all_sql_widgets_html(
        [
            weather_current_html.key,
            # weather_daily_html.key
            football_latest_result_html.key,
            football_next_fixture_html.key,
        ]
    )
    left_widgets = [datetime_widget] + get_all_sql_widgets_html(
        [
            tfl_departures_html.key,
            tfl_status_html.key,
            bins_html.key,
        ]
    )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "left_widgets": left_widgets,
            "right_widgets": right_widgets,
        },
    )
