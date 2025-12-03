import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException, 
    TimeoutException, 
    NoSuchElementException
)
from data.test_data import TestData


class BasePage:
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
    
    @allure.step("Найти элемент")
    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))
    
    @allure.step("Найти несколько элементов")
    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    @allure.step("Кликнуть на элемент")
    def click_element(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except ElementClickInterceptedException:
            self.execute_script("arguments[0].click();", element)
    
    @allure.step("Ввести текст в поле")
    def send_keys(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    @allure.step("Получить текст элемента")
    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text
    
    @allure.step("Проверить видимость элемента")
    def is_element_visible(self, locator, timeout=None):
        try:
            wait = WebDriverWait(self.driver, timeout or TestData.DEFAULT_TIMEOUT)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    @allure.step("Проверить присутствие элемента")
    def is_element_present(self, locator):
        try:
            self.find_element(locator)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    @allure.step("Ожидать исчезновения элемента")
    def wait_for_element_to_disappear(self, locator, timeout=None):
        wait = WebDriverWait(self.driver, timeout or TestData.DEFAULT_TIMEOUT)
        wait.until(EC.invisibility_of_element_located(locator))
    
    @allure.step("Прокрутить к элементу")
    def scroll_to_element(self, locator):
        element = self.find_element(locator)
        self.execute_script("arguments[0].scrollIntoView();", element)
    
    @allure.step("Ожидать, что URL содержит подстроку")
    def wait_for_url_contains(self, url_part, timeout=None):
        wait = WebDriverWait(self.driver, timeout or TestData.DEFAULT_TIMEOUT)
        wait.until(EC.url_contains(url_part))
    
    @allure.step("Перейти на URL")
    def navigate_to(self, url):
        self.driver.get(url)
    
    @allure.step("Получить текущий URL")
    def get_current_url(self):
        return self.driver.current_url
    
    @allure.step("Получить атрибут элемента")
    def get_attribute(self, locator, attribute):
        element = self.find_element(locator)
        return element.get_attribute(attribute)
    
    @allure.step("Проверить активность поля ввода")
    def is_element_active(self, locator):
        element = self.find_element(locator)
        classes = element.get_attribute("class")
        return "input_status_active" in classes or "input__status_active" in classes
    
    @allure.step("Ожидать загрузки страницы")
    def wait_for_page_load(self, timeout=None):
        wait = WebDriverWait(self.driver, timeout or TestData.DEFAULT_TIMEOUT)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    
    @allure.step("Ожидать видимости элемента")
    def wait_for_element_visible(self, locator, timeout=None):
        wait = WebDriverWait(self.driver, timeout or TestData.DEFAULT_TIMEOUT)
        wait.until(EC.visibility_of_element_located(locator))
    
    @allure.step("Ожидать кликабельности элемента")
    def wait_for_element_clickable(self, locator, timeout=None):
        wait = WebDriverWait(self.driver, timeout or TestData.DEFAULT_TIMEOUT)
        wait.until(EC.element_to_be_clickable(locator))
    
    @allure.step("Выполнить JavaScript")
    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)
    
    @allure.step("Ожидать выполнения условия")
    def wait_until(self, condition, timeout=None):
        wait = WebDriverWait(self.driver, timeout or TestData.DEFAULT_TIMEOUT)
        return wait.until(condition)
    
    @allure.step("Закрыть модальное окно")
    def close_modal(self, close_button_locator, modal_locator, timeout=None):
        if timeout is None:
            timeout = TestData.MODAL_TIMEOUT
        element = self.find_element(close_button_locator)
        self.execute_script("arguments[0].click();", element)
        try:
            self.wait_for_element_to_disappear(modal_locator, timeout=timeout)
        except TimeoutException:
            pass
    
    @allure.step("Проверить видимость модального окна")
    def is_modal_visible(self, modal_locator, timeout=None):
        if timeout is None:
            timeout = TestData.SHORT_TIMEOUT
        return self.is_element_visible(modal_locator, timeout=timeout)
