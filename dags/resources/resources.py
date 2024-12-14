from contextlib import contextmanager
import dagster as dg
from pydantic import PrivateAttr
from selenium.webdriver.chrome.webdriver import WebDriver

from resources.selenium import SeleniumDriver

class SeleniumResource(dg.ConfigurableResource):
    _driver: WebDriver = PrivateAttr()

    @contextmanager
    def yield_for_execution(self, context: dg.InitResourceContext):
        with SeleniumDriver() as driver:
            self._driver = driver
            yield self
