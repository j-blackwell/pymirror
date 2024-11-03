import pandas as pd
import os
from widgets.bins.bins_html import bins_html
from resources.selenium import SeleniumDriver
from resources.sqlite import update_sql_widget
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import StringIO

POST_CODE = os.environ["POST_CODE"].strip('"')


def update_bins():
    raw_df = get_bins()
    bins_df = transform_bins(raw_df)
    update_sql_widget("bins", bins_df, bins_html)


def get_bins():
    with SeleniumDriver() as driver:
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
        df = pd.read_html(StringIO(table.get_attribute("outerHTML")))[0]

    return df


def transform_bins(raw_df):
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


if __name__ == "__main__":
    update_bins()
