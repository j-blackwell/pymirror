from contextlib import contextmanager
import dagster as dg
from pydantic import PrivateAttr
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class SeleniumResource(dg.ConfigurableResource):
    _driver: WebDriver = PrivateAttr()

    def _set_options(self):
        self.options = ChromeOptions()

    def _set_driver(self):
        self._set_options()
        driver_service = Service(ChromeDriverManager().install())
        self._driver = webdriver.Chrome(service=driver_service, options=self.options)

    @contextmanager
    def yield_for_execution(self, context: dg.InitResourceContext):
        self._set_driver()
        yield self
        self._driver.close()
