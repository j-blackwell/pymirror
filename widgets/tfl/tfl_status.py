import pandas as pd
import os
import requests
from resources.selenium import SeleniumDriver
from resources.sqlite import update_sql_widget

TFL_LINE_IDS = os.getenv("TFL_LINE_IDS")


def update_tfl_status():
    line_ids = TFL_LINE_IDS.split(",")
    line_status_info = [{"line": line,  **get_tfl_status(line)} for line in line_ids]
    line_status_df = transform_tfl_status(line_status_info)
    update_sql_widget("line_status", line_status_df, pd.DataFrame.to_html, index=False)

def get_tfl_status(line_id):
    # Define the URL to fetch line status
    url = f"https://api.tfl.gov.uk/Line/{line_id}/Status"
    
    # Send the request and get the response
    response = requests.get(url)
    
    # Check if the request was successful (HTTP Status Code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        line_status = data[0]['lineStatuses'][0]['statusSeverityDescription']
        line_status_details = data[0]['lineStatuses'][0].get('reason', 'No further details provided')
        
        return {"status": line_status, "details": line_status_details}
    else:
        # Handle possible errors, such as API changes or network issues
        print(f"Failed to retrieve data: {response.status_code}")
        return {"status": None, "details": None}
    
def transform_tfl_status(raw_df):
    return pd.DataFrame(raw_df)

if __name__ == "__main__":
    update_tfl_status()