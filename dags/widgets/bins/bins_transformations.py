import os
import pandas as pd
from selenium.webdriver.chrome.webdriver import WebDriver
from dags.resources.io_managers import HTML
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import StringIO


POST_CODE = os.environ["POST_CODE"].strip('"')
BIN_MAPPING = {
    "BLACK RUBBISH WHEELIE BIN": "Rubbish",
    "BLUE RECYCLING WHEELIE BIN": "Recycling",
    "FOOD BOX": "Food",
}

def get_bins_raw(driver: WebDriver) -> pd.DataFrame:
    driver.get("https://www.ealing.gov.uk/site/custom_scripts/wasteCollectionWS/")
    driver.find_element(By.ID, "Postcode").send_keys(POST_CODE)
    driver.find_element(By.ID, "btnGet").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//select[@id='Address']/option[2]")
        )
    )
    select = Select(driver.find_element(By.ID, "Address"))
    select.select_by_index(1)
    driver.find_element(By.ID, "btnShowCollection").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//table[@id='Ctable']/tbody/tr[not(.='')]")
        )
    )
    table = driver.find_element(By.ID, "Ctable")
    bins_raw = pd.read_html(StringIO(table.get_attribute("outerHTML")))[0]

    return bins_raw


def transform_bins_data(raw_df):
    bins_df = (
        raw_df.rename({"Container type": "bin"}, axis=1)
        .rename({"Next collection": "next_collection_str"}, axis=1)
        .assign(next_collection_str=lambda df: df["next_collection_str"].str.split(" "))
        .explode("next_collection_str")
        .drop_duplicates()
        .assign(
            next_collection=lambda df: pd.to_datetime(
                df["next_collection_str"], format="%d/%m/%Y"
            )
        )
        .assign(
            next_collection_days=lambda df: (
                df["next_collection"] - pd.Timestamp.today()
            ).dt.days
        )
        .drop(["next_collection_str"], axis=1)
    )

    return bins_df


def transform_bins_html(df: pd.DataFrame) -> HTML:
    df = df.assign(bin_short=lambda df: df["bin"].map(BIN_MAPPING)).sort_values(
        ["next_collection_days"]
    )

    html_all = "<h3>Bins</h3>\n<ul>"
    for idx, row in df.iterrows():
        html_all += (
            f"\n<li>{row['bin_short']} - {row['next_collection_days']} days</li>"
        )

    return HTML(html_all)
