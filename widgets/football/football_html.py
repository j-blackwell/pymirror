import pandas as pd
import os

IMAGES = {
    "Brentford": "https://www.vectorkhazana.com/assets/images/products/Brentford_fc_Black.png"
}


def football_latest_result_html(df: pd.DataFrame) -> str:
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

    return html_all

def football_next_fixture_html(df: pd.DataFrame) -> str:
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

    return html_all