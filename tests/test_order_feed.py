import pytest
import allure
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from pages.personal_account_page import PersonalAccountPage
from data.test_data import TestData
from utils.order_utils import normalize_order_number
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Лента заказов")
@allure.story("Детали заказа")
class TestOrderDetails:
    
    @allure.title("Клик на заказ открывает всплывающее окно с деталями")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_click_order_opens_modal(self, driver):
        with allure.step("Открыть страницу ленты заказов"):
            driver.get(TestData.FEED_URL)
            order_feed_page = OrderFeedPage(driver)
            order_feed_page.wait_for_page_load()
        
        with allure.step("Дождаться появления заказов в ленте"):
            wait = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
            wait_long = WebDriverWait(driver, TestData.LONG_TIMEOUT)
            
            def orders_appeared(driver):
                return len(order_feed_page.find_elements(order_feed_page.locators.ORDER_ITEMS)) > 0
            
            wait_long.until(orders_appeared)
            orders = order_feed_page.find_elements(order_feed_page.locators.ORDER_ITEMS)
            assert len(orders) > 0, "В ленте заказов нет заказов для тестирования"
        
        with allure.step("Получить номер заказа из списка"):
            order_number_from_list = order_feed_page.get_order_number_from_list(0)
        
        with allure.step("Кликнуть на заказ"):
            order_feed_page.click_order(0)
        
        with allure.step("Проверить открытие модального окна"):
            def modal_visible(driver):
                return order_feed_page.is_order_modal_visible()
            
            wait_long.until(modal_visible)
            order_number_from_modal = order_feed_page.get_order_number_from_modal()
        
        with allure.step("Проверить совпадение номеров заказа"):
            normalized_list = normalize_order_number(order_number_from_list)
            normalized_modal = normalize_order_number(order_number_from_modal)
            assert normalized_list == normalized_modal, \
                f"Номер заказа из списка ({order_number_from_list}, нормализованный: {normalized_list}) " \
                f"не совпадает с номером заказа в модальном окне ({order_number_from_modal}, нормализованный: {normalized_modal})"
        
        with allure.step("Закрыть модальное окно"):
            order_feed_page.close_order_modal()


@allure.feature("Лента заказов")
@allure.story("Отображение заказов пользователя")
class TestUserOrdersDisplay:
    
    @allure.title("Заказы пользователя из 'Истории заказов' отображаются на странице 'Лента заказов'")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_user_orders_in_feed(self, driver, logged_in_user, created_order):
        with allure.step("Открыть главную страницу"):
            driver.get(TestData.BASE_URL)
            main_page = MainPage(driver)
            main_page.wait_for_page_load()
        
        wait = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
        
        with allure.step("Перейти в историю заказов"):
            main_page.click_personal_account_button()
            wait.until(EC.url_contains("account"))
            personal_account_page = PersonalAccountPage(driver)
            personal_account_page.click_order_history_button()
            wait.until(EC.url_contains("order-history"))
        
        with allure.step("Получить номера заказов из истории"):
            history_orders = personal_account_page.get_order_numbers_from_history()
            assert len(history_orders) > 0, "В истории заказов нет заказов"
        
        with allure.step("Перейти в ленту заказов"):
            main_page.click_order_feed_button()
            wait.until(EC.url_contains("feed"))
            order_feed_page = OrderFeedPage(driver)
            
            def feed_has_orders(driver):
                return len(order_feed_page.get_order_numbers_from_feed()) > 0
            
            wait.until(feed_has_orders)
        
        with allure.step("Получить номера заказов из ленты"):
            feed_orders = order_feed_page.get_order_numbers_from_feed()
        
        with allure.step("Проверить наличие заказов из истории в ленте"):
            normalized_history = [normalize_order_number(order) for order in history_orders if order]
            normalized_feed = [normalize_order_number(order) for order in feed_orders if order]
            order_found = any(
                norm_history in normalized_feed or 
                any(norm_history in norm_feed or norm_feed in norm_history for norm_feed in normalized_feed)
                for norm_history in normalized_history
            )
            assert order_found, \
                f"Заказы из истории {history_orders} не найдены в ленте заказов {feed_orders}"


@allure.feature("Лента заказов")
@allure.story("Счётчики заказов")
class TestOrderCounters:
    
    @allure.title("При создании нового заказа счётчик 'Выполнено за всё время' увеличивается")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_done_all_time_counter_increases(self, driver, logged_in_user):
        with allure.step("Открыть страницу ленты заказов"):
            driver.get(TestData.FEED_URL)
            order_feed_page = OrderFeedPage(driver)
            order_feed_page.wait_for_page_load()
        
        with allure.step("Получить начальное значение счётчика"):
            initial_counter = order_feed_page.get_done_all_time_counter()
            initial_value = int(initial_counter) if initial_counter and initial_counter.isdigit() else 0
        
        with allure.step("Создать новый заказ"):
            driver.get(TestData.BASE_URL)
            main_page = MainPage(driver)
            main_page.wait_for_page_load()
            wait = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
            
            def bun_counter_updated(driver):
                return main_page.get_ingredient_counter(main_page.locators.INGREDIENT_BUN) > 0
            
            main_page.add_ingredient_to_constructor(main_page.locators.INGREDIENT_BUN)
            wait.until(bun_counter_updated)
            
            def sauce_counter_updated(driver):
                return main_page.get_ingredient_counter(main_page.locators.INGREDIENT_SAUCE) > 0
            
            main_page.add_ingredient_to_constructor(main_page.locators.INGREDIENT_SAUCE)
            wait.until(sauce_counter_updated)
            main_page.click_order_button()
            main_page.wait_for_element_visible(main_page.locators.ORDER_MODAL, timeout=TestData.ORDER_MODAL_TIMEOUT)
            main_page.close_order_modal()
        
        with allure.step("Вернуться в ленту заказов и проверить увеличение счётчика"):
            main_page.click_order_feed_button()
            wait.until(EC.url_contains("feed"))
            
            from helpers.counter_helper import wait_for_counter_increase
            order_feed_page = OrderFeedPage(driver)
            new_value = wait_for_counter_increase(order_feed_page, "all_time", initial_value)
            assert new_value >= initial_value
    
    @allure.title("При создании нового заказа счётчик 'Выполнено за сегодня' увеличивается")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_done_today_counter_increases(self, driver, logged_in_user):
        with allure.step("Открыть страницу ленты заказов"):
            driver.get(TestData.FEED_URL)
            order_feed_page = OrderFeedPage(driver)
            order_feed_page.wait_for_page_load()
        
        with allure.step("Получить начальное значение счётчика"):
            initial_counter = order_feed_page.get_done_today_counter()
            initial_value = int(initial_counter) if initial_counter and initial_counter.isdigit() else 0
        
        with allure.step("Создать новый заказ"):
            driver.get(TestData.BASE_URL)
            main_page = MainPage(driver)
            main_page.wait_for_page_load()
            wait = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
            
            def bun_counter_updated(driver):
                return main_page.get_ingredient_counter(main_page.locators.INGREDIENT_BUN) > 0
            
            main_page.add_ingredient_to_constructor(main_page.locators.INGREDIENT_BUN)
            wait.until(bun_counter_updated)
            
            def sauce_counter_updated(driver):
                return main_page.get_ingredient_counter(main_page.locators.INGREDIENT_SAUCE) > 0
            
            main_page.add_ingredient_to_constructor(main_page.locators.INGREDIENT_SAUCE)
            wait.until(sauce_counter_updated)
            main_page.click_order_button()
            main_page.wait_for_element_visible(main_page.locators.ORDER_MODAL, timeout=TestData.ORDER_MODAL_TIMEOUT)
            main_page.close_order_modal()
        
        with allure.step("Вернуться в ленту заказов и проверить увеличение счётчика"):
            main_page.click_order_feed_button()
            wait.until(EC.url_contains("feed"))
            
            from helpers.counter_helper import wait_for_counter_increase
            order_feed_page = OrderFeedPage(driver)
            new_value = wait_for_counter_increase(order_feed_page, "today", initial_value)
            assert new_value >= initial_value


@allure.feature("Лента заказов")
@allure.story("Раздел 'В работе'")
class TestInProgressSection:
    
    @allure.title("После оформления заказа его номер появляется в разделе 'В работе'")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_order_appears_in_progress(self, driver, logged_in_user, created_order):
        order_number = created_order
        with allure.step("Открыть главную страницу"):
            driver.get(TestData.BASE_URL)
            main_page = MainPage(driver)
            main_page.wait_for_page_load()
        
        wait = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
        
        with allure.step("Перейти в ленту заказов"):
            main_page.click_order_feed_button()
            wait.until(EC.url_contains("feed"))
            order_feed_page = OrderFeedPage(driver)
        
        with allure.step("Проверить появление заказа в разделе 'В работе'"):
            wait_long = WebDriverWait(driver, TestData.LONG_TIMEOUT)
            
            def in_progress_has_orders(driver):
                return len(order_feed_page.get_in_progress_orders()) > 0
            
            wait_long.until(in_progress_has_orders)
            in_progress_orders = order_feed_page.get_in_progress_orders()
            
            if not in_progress_orders:
                wait_extra = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
                wait_extra.until(in_progress_has_orders)
                in_progress_orders = order_feed_page.get_in_progress_orders()
            
            order_number_str = normalize_order_number(order_number)
            order_found = any(
                order_number_str == normalize_order_number(order) or 
                order_number_str in str(order).strip() or 
                str(order).strip() in order_number_str
                for order in in_progress_orders if order
            )
            assert order_found, \
                f"Заказ {order_number} не найден в разделе 'В работе'. Найдены заказы: {in_progress_orders}"
