from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime
from resources.sqlite import get_all_sql_widgets_html

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def home(request: Request):
    # Your logic to retrieve and process data goes here
    
    # Example time and date retrieval:
    current_time = datetime.now().strftime("%H:%M")
    current_date = datetime.now().strftime("%Y-%m-%d")
    all_widgets = get_all_sql_widgets_html(["bins", "weather_current", "weather_daily"])
    left_widgets = [
        f"<div>Time: {current_time}</div>",
        f"<div>Date: {current_date}</div>",
        # Add more left widgets here
    ]

    right_widgets = all_widgets

    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "left_widgets": left_widgets, 
            "right_widgets": right_widgets
        })
