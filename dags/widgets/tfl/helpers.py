import pandas as pd
import os
from dotenv import dotenv_values

env = dotenv_values()
TIMEZONE = env["TIMEZONE"]


def convert_tfl_dates(x):
    return pd.to_datetime(
        x, format="%Y-%m-%dT%H:%M:%S%z", errors="coerce"
    ).dt.tz_convert(TIMEZONE)
