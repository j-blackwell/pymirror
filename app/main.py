from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from resources.sqlite import get_all_sql_widgets_html
from widgets.datetime.datetime import get_datetime_widget

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def home(request: Request):
    datetime_widget = get_datetime_widget()
    right_widgets = get_all_sql_widgets_html(
        [
            "weather_current",
            # "weather_daily",
            "football_latest_result",
            "football_next_fixture",
        ]
    )
    left_widgets = [datetime_widget] + get_all_sql_widgets_html(
        ["tfl_departures", "tfl_status", "bins"]
    )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "left_widgets": left_widgets,
            "right_widgets": right_widgets,
        },
    )
