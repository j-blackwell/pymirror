from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumDriver:

    def _set_options(self):
        self.options = ChromeOptions()

    def _set_driver(self):
        self._set_options()
        driver_service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=driver_service, options=self.options)

    # When entering the 'with' block, driver is returned
    def __enter__(self):
        self._set_driver()
        return self.driver

    # Ensures that the driver is closed upon exiting the 'with' block
    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.close()