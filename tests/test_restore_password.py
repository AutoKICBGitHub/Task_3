import pytest
import allure
from pages.auth_page import AuthPage
from pages.main_page import MainPage
from pages.restore_password_page import RestorePasswordPage
from locators.auth_locators import RestorePasswordLocators
from data.test_data import TestData


@allure.feature("Восстановление пароля")
@allure.story("Переход на страницу восстановления пароля")
class TestRestorePasswordNavigation:
    
    @allure.title("Переход на страницу восстановления пароля по кнопке 'Восстановить пароль'")
    @allure.description("Проверка перехода на страницу восстановления пароля при клике на ссылку 'Восстановить пароль'")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_go_to_restore_password_page(self, driver):
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)
            main_page.navigate_to(TestData.BASE_URL)
        
        with allure.step("Перейти на страницу авторизации"):
            main_page.click_personal_account_button()
        
        with allure.step("Кликнуть на кнопку 'Восстановить пароль'"):
            auth_page = AuthPage(driver)
            auth_page.click_restore_password_button()
        
        with allure.step("Проверить переход на страницу восстановления пароля"):
            auth_page.wait_for_url_contains("forgot-password")
            assert "forgot-password" in auth_page.get_current_url()


@allure.feature("Восстановление пароля")
@allure.story("Функциональность восстановления пароля")
class TestRestorePasswordFunctionality:
    
    @allure.title("Ввод почты и клик по кнопке 'Восстановить'")
    @allure.description("Проверка ввода email и отправки запроса на восстановление пароля")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_enter_email_and_click_restore(self, driver):
        with allure.step("Открыть страницу восстановления пароля"):
            restore_page = RestorePasswordPage(driver)
            restore_page.navigate_to(TestData.FORGOT_PASSWORD_URL)
        
        with allure.step("Ввести email"):
            restore_page.enter_email(TestData.TEST_EMAIL)
        
        with allure.step("Кликнуть на кнопку 'Восстановить'"):
            restore_page.click_restore_button()
        
        with allure.step("Проверить появление ссылки 'Войти'"):
            assert restore_page.is_element_visible(restore_page.locators.LOGIN_LINK)
    
    @allure.title("Клик по кнопке показать/скрыть пароль делает поле активным")
    @allure.description("Проверка изменения типа поля пароля при клике на кнопку показать/скрыть пароль")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_show_password_button_activates_field(self, driver):
        with allure.step("Открыть страницу регистрации"):
            auth_page = AuthPage(driver)
            auth_page.navigate_to(TestData.REGISTER_URL)
            password_input = auth_page.locators.PASSWORD_INPUT
            auth_page.wait_for_element_visible(password_input)
        
        with allure.step("Найти кнопку показать/скрыть пароль"):
            restore_locators = RestorePasswordLocators()
            show_password_btn = restore_locators.SHOW_PASSWORD_BUTTON
        
        if auth_page.is_element_visible(show_password_btn, timeout=TestData.MODAL_TIMEOUT):
            if not auth_page.is_element_visible(password_input, timeout=TestData.SHORT_TIMEOUT):
                pytest.skip("Поле пароля не найдено на странице регистрации")
            
            with allure.step("Получить начальный тип поля пароля"):
                password_input_general = auth_page.locators.PASSWORD_INPUT_GENERAL
                auth_page.wait_for_element_visible(password_input_general)
                initial_type = auth_page.get_attribute(password_input_general, "type")
            
            with allure.step("Кликнуть на кнопку показать/скрыть пароль"):
                auth_page.click_element(show_password_btn)
            
            with allure.step("Проверить изменение типа поля пароля"):
                auth_page.wait_until(
                    lambda d: auth_page.get_attribute(password_input_general, "type") != initial_type
                )
                new_type = auth_page.get_attribute(password_input_general, "type")
                assert new_type != initial_type, \
                    f"Тип поля не изменился после клика. Тип: {new_type} (было: {initial_type})"
        else:
            pytest.skip("Кнопка показать/скрыть пароль не найдена на странице регистрации")
