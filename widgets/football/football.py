import pandas as pd
import os
import requests
from dotenv import load_dotenv
from resources.sqlite import update_sql_widget

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
load_dotenv(dotenv_path)
TEAM_ID = os.getenv("TEAM_ID")


def update_football_matches():
    matches = get_football_matches()
    latest_result, next_fixture = transform_football_matches(matches)
    update_sql_widget("football_latest_result", latest_result, pd.DataFrame.to_html, index=False)
    update_sql_widget("football_next_fixture", next_fixture, pd.DataFrame.to_html, index=False)


def get_football_matches():
    url = f"https://fbref.com/en/squads/{TEAM_ID}"
    response = requests.get(url)
    matches = pd.read_html(response.content)[1]
    return matches

def transform_football_matches(matches):
    latest_result = (
        matches
        .loc[lambda df: df["Result"].notna()]
        .assign(datetime=lambda df: df["Date"] + " " + df["Time"])
        .tail(1)
        [["datetime", "Comp", "Venue", "Opponent", "GF", "GA", "xG", "xGA"]]
    )

    next_fixture = (
        matches
        .loc[lambda df: df["Result"].isna()]
        .assign(datetime=lambda df: df["Date"] + " " + df["Time"])
        .head(1)
        [["datetime", "Comp", "Venue", "Opponent"]]
    )

    return latest_result, next_fixture


if __name__ == "__main__":
    update_football_matches()