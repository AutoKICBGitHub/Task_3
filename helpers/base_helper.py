from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException
from data.test_data import TestData


class BaseHelper:
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
    
    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    def click_element(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)
    
    def send_keys(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text
    
    def is_element_visible(self, locator, timeout=None):
        try:
            wait = WebDriverWait(self.driver, timeout or TestData.DEFAULT_TIMEOUT)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator):
        try:
            self.find_element(locator)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def wait_for_element_to_disappear(self, locator, timeout=None):
        wait = WebDriverWait(self.driver, timeout or TestData.DEFAULT_TIMEOUT)
        wait.until(EC.invisibility_of_element_located(locator))
    
    def scroll_to_element(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
    
    def wait_for_url_contains(self, url_part, timeout=None):
        wait = WebDriverWait(self.driver, timeout or TestData.DEFAULT_TIMEOUT)
        wait.until(EC.url_contains(url_part))
    
    def get_current_url(self):
        return self.driver.current_url
    
    def get_attribute(self, locator, attribute):
        element = self.find_element(locator)
        return element.get_attribute(attribute)
    
    def is_element_active(self, locator):
        element = self.find_element(locator)
        classes = element.get_attribute("class")
        return "input_status_active" in classes or "input__status_active" in classes
    
    def wait_for_page_load(self, timeout=None):
        wait = WebDriverWait(self.driver, timeout or TestData.DEFAULT_TIMEOUT)
        
        def page_loaded(driver):
            return driver.execute_script("return document.readyState") == "complete"
        
        wait.until(page_loaded)
    
    def wait_for_element_visible(self, locator, timeout=None):
        wait = WebDriverWait(self.driver, timeout or TestData.DEFAULT_TIMEOUT)
        wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_element_clickable(self, locator, timeout=None):
        wait = WebDriverWait(self.driver, timeout or TestData.DEFAULT_TIMEOUT)
        wait.until(EC.element_to_be_clickable(locator))
