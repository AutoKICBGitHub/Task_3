import pytest
import allure
from pages.main_page import MainPage
from pages.personal_account_page import PersonalAccountPage
from data.test_data import TestData
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Личный кабинет")
@allure.story("Навигация в личный кабинет")
class TestPersonalAccountNavigation:
    
    @allure.title("Переход по клику на 'Личный кабинет'")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_go_to_personal_account(self, driver, logged_in_user):
        with allure.step("Открыть главную страницу"):
            driver.get(TestData.BASE_URL)
            main_page = MainPage(driver)
        
        with allure.step("Кликнуть на кнопку 'Личный кабинет'"):
            main_page.click_personal_account_button()
        
        with allure.step("Проверить переход в личный кабинет"):
            wait = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
            
            def url_contains_account(driver):
                return "account" in driver.current_url or "profile" in driver.current_url
            
            wait.until(url_contains_account)
            assert "account" in driver.current_url or "profile" in driver.current_url


@allure.feature("Личный кабинет")
@allure.story("История заказов")
class TestOrderHistory:
    
    @allure.title("Переход в раздел 'История заказов'")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_go_to_order_history(self, driver, logged_in_user):
        with allure.step("Открыть главную страницу"):
            driver.get(TestData.BASE_URL)
            main_page = MainPage(driver)
        
        with allure.step("Перейти в личный кабинет"):
            main_page.click_personal_account_button()
            wait = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
            wait.until(EC.url_contains("account"))
        
        with allure.step("Кликнуть на кнопку 'История заказов'"):
            personal_account_page = PersonalAccountPage(driver)
            personal_account_page.click_order_history_button()
        
        with allure.step("Проверить переход в раздел истории заказов"):
            wait.until(EC.url_contains("order-history"))
            assert personal_account_page.is_order_history_visible()


@allure.feature("Личный кабинет")
@allure.story("Выход из аккаунта")
class TestLogout:
    
    @allure.title("Выход из аккаунта")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_logout(self, driver, logged_in_user):
        with allure.step("Открыть главную страницу"):
            driver.get(TestData.BASE_URL)
            main_page = MainPage(driver)
        
        with allure.step("Перейти в личный кабинет"):
            main_page.click_personal_account_button()
            wait = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
            wait.until(EC.url_contains("account"))
        
        with allure.step("Кликнуть на кнопку 'Выход'"):
            personal_account_page = PersonalAccountPage(driver)
            personal_account_page.click_logout_button()
        
        with allure.step("Проверить переход на страницу авторизации"):
            wait.until(EC.url_contains("login"))
            assert "login" in driver.current_url
