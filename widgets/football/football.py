import pandas as pd
import numpy as np
import os
import requests
import re
from bs4 import BeautifulSoup
from dotenv import dotenv_values
from resources.sqlite import update_sql_widget
from widgets.football.football_html import (
    football_latest_result_html,
    football_next_fixture_html,
)

TEAM_ID = dotenv_values()["TEAM_ID"]

POINTS_MAPPING = {"W": 3, "D": 1, "L": 0}


def update_football_matches():
    matches, matches_prev = get_football_matches()
    latest_result, next_fixture, result_comparison = transform_football_matches(
        matches, matches_prev
    )
    update_sql_widget(
        "football_latest_result", latest_result, football_latest_result_html
    )
    update_sql_widget("football_next_fixture", next_fixture, football_next_fixture_html)
    update_sql_widget(
        "football_result_comparison",
        result_comparison,
        pd.DataFrame.to_html,
        index=False,
    )


def get_team_matches(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="lxml")
    matches = pd.read_html(response.content)[1]
    h1 = soup.find("h1").text
    team_name = re.search("[0-9]{4}-[0-9]{4} (.*) Stats", h1).group(1)
    matches["Team"] = team_name

    return matches, soup


def get_football_matches():
    # this season
    url = f"https://fbref.com/en/squads/{TEAM_ID}"
    matches, soup = get_team_matches(url)

    # prev season
    endpoint = soup.find("div", attrs={"class": "prevnext"}).find("a").attrs["href"]
    url_prev = f"https://fbref.com" + endpoint
    matches_prev, _ = get_team_matches(url_prev)

    return matches, matches_prev


def transform_football_matches(matches, matches_prev):
    home_away_matches = (
        matches.assign(
            home_team=lambda df: np.where(
                df["Venue"] == "Home", df["Team"], df["Opponent"]
            )
        )
        .assign(
            away_team=lambda df: np.where(
                df["Venue"] == "Home", df["Opponent"], df["Team"]
            )
        )
        .assign(home_g=lambda df: np.where(df["Venue"] == "Home", df["GF"], df["GA"]))
        .assign(away_g=lambda df: np.where(df["Venue"] == "Home", df["GA"], df["GF"]))
        .assign(home_xg=lambda df: np.where(df["Venue"] == "Home", df["xG"], df["xGA"]))
        .assign(away_xg=lambda df: np.where(df["Venue"] == "Home", df["xGA"], df["xG"]))
    )

    result_comparison = (
        matches_prev        .merge(
            matches,
            how="right",
            left_on=["Comp", "Venue", "Opponent"],
            right_on=["Comp", "Venue", "Opponent"],
            suffixes=("_prev", ""),
        )
        .assign(points=lambda df: df["Result"].map(POINTS_MAPPING))
        .assign(points_prev=lambda df: df["Result_prev"].map(POINTS_MAPPING))
        .assign(points_diff=lambda df: df["points"] - df["points_prev"])
        .loc[lambda df: df["Comp"] == "Premier League"][
            # .loc[lambda df: df["points_diff"].notna()]
            [
                "Comp",
                "Opponent",
                "Venue",
                "Result",
                "Result_prev",
                "points",
                "points_prev",
                "points_diff",
            ]
        ]
    )

    latest_result = (
        home_away_matches.loc[lambda df: df["Result"].notna()]
        .assign(datetime=lambda df: df["Date"] + " " + df["Time"])
        .tail(1)[
            [
                "datetime",
                "home_team",
                "away_team",
                "home_g",
                "away_g",
                "home_xg",
                "away_xg",
            ]
        ]
    )

    form = home_away_matches.loc[lambda df: df["Result"].notna()]["Result"][-5:]

    next_fixture = (
        home_away_matches.loc[lambda df: df["Result"].isna()]
        .head(1)
        .merge(
            result_comparison,
            how="left",
            left_on=["Comp", "Opponent", "Venue"],
            right_on=["Comp", "Opponent", "Venue"],
        )
        .assign(datetime=lambda df: df["Date"] + " " + df["Time"])
        .assign(form="".join(form))[
            ["datetime", "home_team", "away_team", "form", "Result_prev"]
        ]
    )

    return latest_result, next_fixture, result_comparison


if __name__ == "__main__":
    update_football_matches()
