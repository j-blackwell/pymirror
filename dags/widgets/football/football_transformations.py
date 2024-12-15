import os
import re

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import dotenv_values

from dags.resources.io_managers import HTML

TEAM_ID = dotenv_values()["TEAM_ID"]
POINTS_MAPPING = {"W": 3, "D": 1, "L": 0}
IMAGES = {
    "Brentford": "https://www.vectorkhazana.com/assets/images/products/Brentford_fc_Black.png"
}


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
        matches_prev.merge(
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


def transform_football_latest_result_html(df: pd.DataFrame) -> HTML:
    row = df.iloc[0]
    html_all = f"""<div class="football">
    <h3>Latest Result</h3>
    <div class="home-team">
        <span>{row["home_team"]}</span>
        <span><img src={IMAGES.get(row["home_team"])} width="50" id="{IMAGES.get(row["home_team"])}"></span>
    </div>
    <div class="score">
        <span>{row["home_g"]}</span>
        <span>({row["home_xg"]} - {row["away_xg"]})</span>
        <span>{row["away_g"]}</span>
    </div>
    <div class="away-team">
        <span>{row["away_team"]}</span>
        <span><img src={IMAGES.get(row["away_team"])} width="50" id="{IMAGES.get(row["away_team"])}"></span>
    </div>
    </div>
    """

    return HTML(html_all)


def transform_football_next_fixture_html(df: pd.DataFrame) -> HTML:
    row = df.iloc[0]
    html_all = f"""<div class="football">
    <h3>Next Fixture</h3>
    <div class="home-team">
        <span>{row["home_team"]}</span>
        <span><img src={IMAGES.get(row["home_team"])} width="50" id="{IMAGES.get(row["home_team"])}"></span>
    </div>
    <div class="preview">
        <span>{row["datetime"]}</span>
        <span>{row["form"]}</span>
        <span>Last time: {row["Result_prev"]}</span>
    </div>
    <div class="away-team">
        <span>{row["away_team"]}</span>
        <span><img src={IMAGES.get(row["away_team"])} width="50" id="{IMAGES.get(row["away_team"])}"></span>
    </div>
    </div>
    """

    return HTML(html_all)

def transform_football_result_comparison_html(df: pd.DataFrame) -> HTML:
    return HTML(df.to_html(index=False))
