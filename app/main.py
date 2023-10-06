from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime
from resources.sqlite import get_all_sql_widgets_html
from widgets.datetime.datetime import get_datetime_widget

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def home(request: Request):
    # Your logic to retrieve and process data goes here
    
    # Example time and date retrieval:
    datetime_widget = get_datetime_widget()
    right_widgets = get_all_sql_widgets_html(["bins", "weather_current", "weather_daily"])
    left_widgets = [datetime_widget] + get_all_sql_widgets_html(["tfl_status"])


    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "left_widgets": left_widgets, 
            "right_widgets": right_widgets
        })
