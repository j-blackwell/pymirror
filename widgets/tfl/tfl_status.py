import datetime as dt
import pandas as pd
import os
import requests
from glom import glom
from dotenv import dotenv_values

from resources.sqlite import update_sql_widget
from widgets.tfl.helpers import convert_tfl_dates
from widgets.tfl.tfl_html import status_html

env = dotenv_values()
TFL_LINE_IDS = env["TFL_LINE_IDS"]
TIMEZONE = env["TIMEZONE"]


def update_tfl_status():
    line_status_info = get_tfl_status(TFL_LINE_IDS)
    line_status_df = transform_tfl_status(line_status_info)
    update_sql_widget("tfl_status", line_status_df, status_html)


def get_tfl_status(line_ids):
    # Define the URL to fetch line status
    url = f"https://api.tfl.gov.uk/Line/{line_ids}/Status"

    # Send the request and get the response
    response = requests.get(url)

    # Check if the request was successful (HTTP Status Code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        line_status = [
            {
                "line": glom(status, "name"),
                "status": glom(
                    status, "lineStatuses.0.statusSeverityDescription", default="None"
                ),
                "disruption": glom(
                    status,
                    "lineStatuses.0.disruption.categoryDescription",
                    default="None",
                ),
                "reason": glom(
                    status, "lineStatuses.0.disruption.description", default="None"
                ),
                "validity_from": glom(
                    status, "lineStatuses.0.validityPeriods.0.fromDate", default="None"
                ),
                "validity_to": glom(
                    status, "lineStatuses.0.validityPeriods.0.toDate", default="None"
                ),
            }
            for status in data
        ]

        return line_status
    else:
        # Handle possible errors, such as API changes or network issues
        print(f"Failed to retrieve data: {response.status_code}")
        return {"status": None, "details": None}


def transform_tfl_status(line_status):
    df = (
        pd.DataFrame(line_status)
        .assign(validity_from=lambda df: convert_tfl_dates(df["validity_from"]))
        .assign(validity_to=lambda df: convert_tfl_dates(df["validity_to"]))
    )
    return df


if __name__ == "__main__":
    update_tfl_status()
