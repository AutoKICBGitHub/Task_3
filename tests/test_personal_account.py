import pytest
import allure
from pages.main_page import MainPage
from pages.personal_account_page import PersonalAccountPage
from data.test_data import TestData


@allure.feature("Личный кабинет")
@allure.story("Навигация в личный кабинет")
class TestPersonalAccountNavigation:
    
    @allure.title("Переход по клику на 'Личный кабинет'")
    @allure.description("Проверка перехода в личный кабинет при клике на кнопку 'Личный кабинет' в хедере")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_go_to_personal_account(self, driver, logged_in_user):
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)
            main_page.navigate_to(TestData.BASE_URL)
        
        with allure.step("Кликнуть на кнопку 'Личный кабинет'"):
            main_page.click_personal_account_button()
        
        with allure.step("Проверить переход в личный кабинет"):
            main_page.wait_until(
                lambda d: "account" in main_page.get_current_url() or "profile" in main_page.get_current_url()
            )
            current_url = main_page.get_current_url()
            assert "account" in current_url or "profile" in current_url


@allure.feature("Личный кабинет")
@allure.story("История заказов")
class TestOrderHistory:
    
    @allure.title("Переход в раздел 'История заказов'")
    @allure.description("Проверка перехода в раздел истории заказов из личного кабинета пользователя")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_go_to_order_history(self, driver, logged_in_user):
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)
            main_page.navigate_to(TestData.BASE_URL)
        
        with allure.step("Перейти в личный кабинет"):
            main_page.click_personal_account_button()
            main_page.wait_for_url_contains("account")
        
        with allure.step("Кликнуть на кнопку 'История заказов'"):
            personal_account_page = PersonalAccountPage(driver)
            personal_account_page.click_order_history_button()
        
        with allure.step("Проверить переход в раздел истории заказов"):
            personal_account_page.wait_for_url_contains("order-history")
            assert personal_account_page.is_order_history_visible()


@allure.feature("Личный кабинет")
@allure.story("Выход из аккаунта")
class TestLogout:
    
    @allure.title("Выход из аккаунта")
    @allure.description("Проверка выхода из аккаунта и перехода на страницу авторизации")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_logout(self, driver, logged_in_user):
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)
            main_page.navigate_to(TestData.BASE_URL)
        
        with allure.step("Перейти в личный кабинет"):
            main_page.click_personal_account_button()
            main_page.wait_for_url_contains("account")
        
        with allure.step("Кликнуть на кнопку 'Выход'"):
            personal_account_page = PersonalAccountPage(driver)
            personal_account_page.click_logout_button()
        
        with allure.step("Проверить переход на страницу авторизации"):
            personal_account_page.wait_for_url_contains("login")
            assert "login" in personal_account_page.get_current_url()
