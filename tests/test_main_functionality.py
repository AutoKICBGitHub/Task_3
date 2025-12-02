import pytest
import allure
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from data.test_data import TestData
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Основной функционал")
@allure.story("Навигация")
class TestNavigation:
    
    @allure.title("Переход по клику на 'Конструктор'")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_go_to_constructor(self, driver):
        with allure.step("Открыть страницу ленты заказов"):
            driver.get(TestData.FEED_URL)
            main_page = MainPage(driver)
        
        with allure.step("Кликнуть на кнопку 'Конструктор'"):
            main_page.click_constructor_button()
        
        with allure.step("Проверить переход на главную страницу"):
            wait = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
            
            def url_changed(driver):
                return TestData.BASE_URL.rstrip('/') in driver.current_url or driver.current_url == TestData.BASE_URL
            
            wait.until(url_changed)
            assert TestData.BASE_URL == driver.current_url.rstrip('/') or "stellarburgers" in driver.current_url
    
    @allure.title("Переход по клику на 'Лента заказов'")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_go_to_order_feed(self, driver):
        with allure.step("Открыть главную страницу"):
            driver.get(TestData.BASE_URL)
            main_page = MainPage(driver)
        
        with allure.step("Кликнуть на кнопку 'Лента заказов'"):
            main_page.click_order_feed_button()
        
        with allure.step("Проверить переход на страницу ленты заказов"):
            wait = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
            wait.until(EC.url_contains("feed"))
            assert "feed" in driver.current_url


@allure.feature("Основной функционал")
@allure.story("Работа с ингредиентами")
class TestIngredients:
    
    @allure.title("Клик на ингредиент открывает всплывающее окно с деталями")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_click_ingredient_opens_modal(self, driver):
        with allure.step("Открыть главную страницу"):
            driver.get(TestData.BASE_URL)
            main_page = MainPage(driver)
        
        with allure.step("Кликнуть на ингредиент"):
            main_page.click_ingredient(main_page.locators.INGREDIENT_BUN)
        
        with allure.step("Проверить открытие модального окна"):
            main_page.wait_for_element_visible(main_page.locators.INGREDIENT_DETAILS_MODAL, timeout=TestData.MODAL_TIMEOUT)
            assert main_page.is_ingredient_modal_visible()
        
        with allure.step("Закрыть модальное окно"):
            main_page.close_ingredient_modal()
    
    @allure.title("Всплывающее окно закрывается кликом по крестику")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_close_modal_by_cross(self, driver):
        with allure.step("Открыть главную страницу"):
            driver.get(TestData.BASE_URL)
            main_page = MainPage(driver)
        
        with allure.step("Открыть модальное окно с деталями ингредиента"):
            main_page.click_ingredient(main_page.locators.INGREDIENT_BUN)
            main_page.wait_for_element_visible(main_page.locators.INGREDIENT_DETAILS_MODAL, timeout=TestData.MODAL_TIMEOUT)
            assert main_page.is_ingredient_modal_visible()
        
        with allure.step("Закрыть модальное окно кликом по крестику"):
            main_page.close_ingredient_modal()
            main_page.wait_for_element_to_disappear(main_page.locators.INGREDIENT_DETAILS_MODAL, timeout=TestData.MODAL_TIMEOUT)
        
        with allure.step("Проверить, что модальное окно закрыто"):
            assert not main_page.is_ingredient_modal_visible()
    
    @allure.title("При добавлении ингредиента в заказ увеличивается каунтер")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_ingredient_counter_increases(self, driver):
        with allure.step("Открыть главную страницу"):
            driver.get(TestData.BASE_URL)
            main_page = MainPage(driver)
            main_page.wait_for_page_load()
        
        with allure.step("Получить начальное значение счётчика"):
            initial_counter = main_page.get_ingredient_counter(main_page.locators.INGREDIENT_BUN)
        
        with allure.step("Добавить ингредиент в конструктор"):
            main_page.add_ingredient_to_constructor(main_page.locators.INGREDIENT_BUN)
        
        with allure.step("Проверить увеличение счётчика"):
            wait = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
            
            def counter_increased(driver):
                return main_page.get_ingredient_counter(main_page.locators.INGREDIENT_BUN) > initial_counter
            
            wait.until(counter_increased)
            new_counter = main_page.get_ingredient_counter(main_page.locators.INGREDIENT_BUN)
            assert new_counter > initial_counter


@allure.feature("Основной функционал")
@allure.story("Оформление заказа")
class TestOrderCreation:
    
    @allure.title("Залогиненный пользователь может оформить заказ")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_logged_in_user_can_create_order(self, driver, logged_in_user):
        with allure.step("Открыть главную страницу"):
            driver.get(TestData.BASE_URL)
            main_page = MainPage(driver)
            main_page.wait_for_page_load()
        
        wait = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
        
        with allure.step("Добавить булку в конструктор"):
            main_page.add_ingredient_to_constructor(main_page.locators.INGREDIENT_BUN)
            
            def bun_counter_updated(driver):
                return main_page.get_ingredient_counter(main_page.locators.INGREDIENT_BUN) > 0
            
            wait.until(bun_counter_updated)
        
        with allure.step("Добавить соус в конструктор"):
            main_page.add_ingredient_to_constructor(main_page.locators.INGREDIENT_SAUCE)
            
            def sauce_counter_updated(driver):
                return main_page.get_ingredient_counter(main_page.locators.INGREDIENT_SAUCE) > 0
            
            wait.until(sauce_counter_updated)
        
        with allure.step("Оформить заказ"):
            main_page.click_order_button()
            main_page.wait_for_element_visible(main_page.locators.ORDER_MODAL, timeout=TestData.ORDER_MODAL_TIMEOUT)
        
        with allure.step("Проверить появление модального окна с номером заказа"):
            assert main_page.is_order_modal_visible()
            order_number = main_page.get_order_number()
            assert order_number is not None and order_number != ""
        
        with allure.step("Закрыть модальное окно"):
            main_page.close_order_modal()
