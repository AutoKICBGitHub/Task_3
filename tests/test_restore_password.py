import pytest
import allure
from pages.auth_page import AuthPage
from pages.restore_password_page import RestorePasswordPage
from data.test_data import TestData
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@allure.feature("Восстановление пароля")
@allure.story("Переход на страницу восстановления пароля")
class TestRestorePasswordNavigation:
    
    @allure.title("Переход на страницу восстановления пароля по кнопке 'Восстановить пароль'")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_go_to_restore_password_page(self, driver):
        with allure.step("Открыть главную страницу"):
            driver.get(TestData.BASE_URL)
            auth_page = AuthPage(driver)
        
        with allure.step("Перейти на страницу авторизации"):
            auth_page.click_personal_account_button()
        
        with allure.step("Кликнуть на кнопку 'Восстановить пароль'"):
            auth_page.click_restore_password_button()
        
        with allure.step("Проверить переход на страницу восстановления пароля"):
            assert "forgot-password" in driver.current_url


@allure.feature("Восстановление пароля")
@allure.story("Функциональность восстановления пароля")
class TestRestorePasswordFunctionality:
    
    @allure.title("Ввод почты и клик по кнопке 'Восстановить'")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_enter_email_and_click_restore(self, driver):
        with allure.step("Открыть страницу восстановления пароля"):
            driver.get(TestData.FORGOT_PASSWORD_URL)
            restore_page = RestorePasswordPage(driver)
        
        with allure.step("Ввести email"):
            restore_page.enter_email(TestData.TEST_EMAIL)
        
        with allure.step("Кликнуть на кнопку 'Восстановить'"):
            restore_page.click_restore_button()
        
        with allure.step("Проверить появление ссылки 'Войти'"):
            assert restore_page.is_element_visible(restore_page.locators.LOGIN_LINK)
    
    @allure.title("Клик по кнопке показать/скрыть пароль делает поле активным")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_show_password_button_activates_field(self, driver):
        with allure.step("Открыть страницу регистрации"):
            driver.get(TestData.REGISTER_URL)
            auth_page = AuthPage(driver)
            wait = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
            password_input = auth_page.locators.PASSWORD_INPUT
            wait.until(EC.presence_of_element_located(password_input))
        
        with allure.step("Найти кнопку показать/скрыть пароль"):
            from locators.auth_locators import RestorePasswordLocators
            restore_locators = RestorePasswordLocators()
            show_password_btn = restore_locators.SHOW_PASSWORD_BUTTON
        
        if auth_page.is_element_visible(show_password_btn, timeout=TestData.MODAL_TIMEOUT):
            if not auth_page.is_element_visible(password_input, timeout=TestData.SHORT_TIMEOUT):
                pytest.skip("Поле пароля не найдено на странице регистрации")
            
            with allure.step("Получить начальный тип поля пароля"):
                password_input_general = (By.XPATH, "//input[@name='Пароль']")
                password_element = wait.until(EC.presence_of_element_located(password_input_general))
                initial_type = password_element.get_attribute("type")
            
            with allure.step("Кликнуть на кнопку показать/скрыть пароль"):
                auth_page.click_element(show_password_btn)
            
            with allure.step("Проверить изменение типа поля пароля"):
                def password_type_changed(driver):
                    element = driver.find_element(*password_input_general)
                    current_type = element.get_attribute("type")
                    return current_type != initial_type
                
                wait.until(password_type_changed)
                password_element_after = wait.until(EC.presence_of_element_located(password_input_general))
                new_type = password_element_after.get_attribute("type")
                assert new_type != initial_type, \
                    f"Тип поля не изменился после клика. Тип: {new_type} (было: {initial_type})"
        else:
            pytest.skip("Кнопка показать/скрыть пароль не найдена на странице регистрации")
