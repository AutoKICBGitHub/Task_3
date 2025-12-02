import allure
from helpers.base_helper import BaseHelper
from selenium.common.exceptions import TimeoutException
from data.test_data import TestData


class BasePage(BaseHelper):
    
    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Закрыть модальное окно")
    def close_modal(self, close_button_locator, modal_locator, timeout=None):
        if timeout is None:
            timeout = TestData.MODAL_TIMEOUT
        element = self.find_element(close_button_locator)
        self.driver.execute_script("arguments[0].click();", element)
        try:
            self.wait_for_element_to_disappear(modal_locator, timeout=timeout)
        except TimeoutException:
            pass
    
    @allure.step("Проверить видимость модального окна")
    def is_modal_visible(self, modal_locator, timeout=None):
        if timeout is None:
            timeout = TestData.SHORT_TIMEOUT
        return self.is_element_visible(modal_locator, timeout=timeout)
