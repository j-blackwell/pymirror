import pandas as pd
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
load_dotenv(dotenv_path)
TIMEZONE = os.getenv("TIMEZONE")

def convert_tfl_dates(x):
    return pd.to_datetime(
        x, 
        format="%Y-%m-%dT%H:%M:%S%z", 
        errors="coerce"
    ).dt.tz_convert(TIMEZONE)