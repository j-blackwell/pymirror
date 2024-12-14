import pandas as pd
import datetime as dt
import json
import urllib

import requests
from dotenv import dotenv_values

env = dotenv_values()
WEATHER_API_KEY = env["WEATHER_API_KEY"]
WEATHER_LAT = env["WEATHER_LAT"]
WEATHER_LON = env["WEATHER_LON"]
DESIRED_FIELDS = ["feels_like", "weather", "uvi", "pop"]


def get_weather_raw():
    base_url = "https://api.openweathermap.org/data/3.0/onecall?"
    params = {
        "lat": WEATHER_LAT,
        "lon": WEATHER_LON,
        "exclude": "minutely,hourly",
        "appid": WEATHER_API_KEY,
        "units": "metric",
    }

    query = base_url + urllib.parse.urlencode(params)
    r = requests.get(query)
    weather = json.loads(r.text)
    return weather


def extract_desired(data, desired_fields=DESIRED_FIELDS):
    return {
        **{k: data.get(k) for k in desired_fields},
        "date": dt.datetime.fromtimestamp(data["dt"]),
    }




def process_weather(weather):
    df = (
        pd.DataFrame(weather)
        .rename({"uvi": "uv_index"}, axis=1)
        .rename({"pop": "rain_prob"}, axis=1)
        .assign(rain_prob=lambda df: df["rain_prob"].fillna(0.0))
        .assign(date=lambda df: pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d"))
    )

    if df["feels_like"].dtype != "float64":
        df = df.explode("weather")
        feels_df = pd.json_normalize(df["feels_like"]).add_suffix("_feels_like")
        df_list = [df, feels_df]
        drop_cols = ["feels_like"]
    else:
        df_list = [df]
        drop_cols = []

    weather_df = pd.json_normalize(df["weather"]).add_prefix("weather_")
    df_list.append(weather_df)
    drop_cols.append("weather")

    df = pd.concat(df_list, axis=1)
    df = df.drop(
        drop_cols + ["weather_id", "weather_description", "weather_icon"], axis=1
    )
    return df

def transform_weather_daily(raw_weather):
    daily_weather = [extract_desired(x) for x in raw_weather["daily"]]
    return process_weather(daily_weather)


def transform_weather_current(raw_weather):
    current_weather = extract_desired(raw_weather["current"])
    return process_weather(current_weather)


if __name__ == "__main__":
    update_weather()
