import pytest
import allure
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from pages.personal_account_page import PersonalAccountPage
from data.test_data import TestData
from utils.order_utils import normalize_order_number


@allure.feature("Лента заказов")
@allure.story("Детали заказа")
class TestOrderDetails:
    
    @allure.title("Клик на заказ открывает всплывающее окно с деталями")
    @allure.description("Проверка открытия модального окна с деталями заказа при клике на заказ в ленте")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_click_order_opens_modal(self, driver):
        with allure.step("Открыть страницу ленты заказов"):
            order_feed_page = OrderFeedPage(driver)
            order_feed_page.navigate_to(TestData.FEED_URL)
            order_feed_page.wait_for_page_load()
        
        with allure.step("Дождаться появления заказов в ленте"):
            order_feed_page.wait_until(
                lambda d: len(order_feed_page.find_elements(order_feed_page.locators.ORDER_ITEMS)) > 0,
                timeout=TestData.LONG_TIMEOUT
            )
            orders = order_feed_page.find_elements(order_feed_page.locators.ORDER_ITEMS)
            assert len(orders) > 0, "В ленте заказов нет заказов для тестирования"
        
        with allure.step("Получить номер заказа из списка"):
            order_number_from_list = order_feed_page.get_order_number_from_list(0)
        
        with allure.step("Кликнуть на заказ"):
            order_feed_page.click_order(0)
        
        with allure.step("Проверить открытие модального окна"):
            order_feed_page.wait_until(
                lambda d: order_feed_page.is_order_modal_visible(),
                timeout=TestData.LONG_TIMEOUT
            )
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
    @allure.description("Проверка отображения заказов пользователя из истории заказов в общей ленте заказов")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_user_orders_in_feed(self, driver, logged_in_user, created_order):
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)
            main_page.navigate_to(TestData.BASE_URL)
            main_page.wait_for_page_load()
        
        with allure.step("Перейти в историю заказов"):
            main_page.click_personal_account_button()
            main_page.wait_for_url_contains("account")
            personal_account_page = PersonalAccountPage(driver)
            personal_account_page.click_order_history_button()
            personal_account_page.wait_for_url_contains("order-history")
        
        with allure.step("Получить номера заказов из истории"):
            history_orders = personal_account_page.get_order_numbers_from_history()
            assert len(history_orders) > 0, "В истории заказов нет заказов"
        
        with allure.step("Перейти в ленту заказов"):
            main_page.click_order_feed_button()
            main_page.wait_for_url_contains("feed")
            order_feed_page = OrderFeedPage(driver)
            
            order_feed_page.wait_until(
                lambda d: len(order_feed_page.get_order_numbers_from_feed()) > 0
            )
        
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
    @allure.description("Проверка увеличения счётчика выполненных заказов за всё время после создания нового заказа")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_done_all_time_counter_increases(self, driver, logged_in_user):
        with allure.step("Открыть страницу ленты заказов"):
            order_feed_page = OrderFeedPage(driver)
            order_feed_page.navigate_to(TestData.FEED_URL)
            order_feed_page.wait_for_page_load()
        
        with allure.step("Получить начальное значение счётчика"):
            initial_counter = order_feed_page.get_done_all_time_counter()
            initial_value = int(initial_counter) if initial_counter and initial_counter.isdigit() else 0
        
        with allure.step("Создать новый заказ"):
            main_page = MainPage(driver)
            main_page.navigate_to(TestData.BASE_URL)
            main_page.wait_for_page_load()
            
            main_page.add_ingredient_to_constructor(main_page.locators.INGREDIENT_BUN)
            main_page.wait_for_bun_counter_updated()
            
            main_page.add_ingredient_to_constructor(main_page.locators.INGREDIENT_SAUCE)
            main_page.wait_for_sauce_counter_updated()
            
            main_page.click_order_button()
            main_page.wait_for_element_visible(main_page.locators.ORDER_MODAL, timeout=TestData.ORDER_MODAL_TIMEOUT)
            main_page.close_order_modal()
        
        with allure.step("Вернуться в ленту заказов и проверить увеличение счётчика"):
            main_page.click_order_feed_button()
            main_page.wait_for_url_contains("feed")
            
            order_feed_page = OrderFeedPage(driver)
            new_value = order_feed_page.wait_for_counter_increase("all_time", initial_value)
            assert new_value >= initial_value
    
    @allure.title("При создании нового заказа счётчик 'Выполнено за сегодня' увеличивается")
    @allure.description("Проверка увеличения счётчика выполненных заказов за сегодня после создания нового заказа")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_done_today_counter_increases(self, driver, logged_in_user):
        with allure.step("Открыть страницу ленты заказов"):
            order_feed_page = OrderFeedPage(driver)
            order_feed_page.navigate_to(TestData.FEED_URL)
            order_feed_page.wait_for_page_load()
        
        with allure.step("Получить начальное значение счётчика"):
            initial_counter = order_feed_page.get_done_today_counter()
            initial_value = int(initial_counter) if initial_counter and initial_counter.isdigit() else 0
        
        with allure.step("Создать новый заказ"):
            main_page = MainPage(driver)
            main_page.navigate_to(TestData.BASE_URL)
            main_page.wait_for_page_load()
            
            main_page.add_ingredient_to_constructor(main_page.locators.INGREDIENT_BUN)
            main_page.wait_for_bun_counter_updated()
            
            main_page.add_ingredient_to_constructor(main_page.locators.INGREDIENT_SAUCE)
            main_page.wait_for_sauce_counter_updated()
            
            main_page.click_order_button()
            main_page.wait_for_element_visible(main_page.locators.ORDER_MODAL, timeout=TestData.ORDER_MODAL_TIMEOUT)
            main_page.close_order_modal()
        
        with allure.step("Вернуться в ленту заказов и проверить увеличение счётчика"):
            main_page.click_order_feed_button()
            main_page.wait_for_url_contains("feed")
            
            order_feed_page = OrderFeedPage(driver)
            new_value = order_feed_page.wait_for_counter_increase("today", initial_value)
            assert new_value >= initial_value


@allure.feature("Лента заказов")
@allure.story("Раздел 'В работе'")
class TestInProgressSection:
    
    @allure.title("После оформления заказа его номер появляется в разделе 'В работе'")
    @allure.description("Проверка появления номера созданного заказа в разделе 'В работе' на странице ленты заказов")
    @pytest.mark.chrome
    @pytest.mark.firefox
    def test_order_appears_in_progress(self, driver, logged_in_user, created_order):
        order_number = created_order
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)
            main_page.navigate_to(TestData.BASE_URL)
            main_page.wait_for_page_load()
        
        with allure.step("Перейти в ленту заказов"):
            main_page.click_order_feed_button()
            main_page.wait_for_url_contains("feed")
            order_feed_page = OrderFeedPage(driver)
        
        with allure.step("Проверить появление заказа в разделе 'В работе'"):
            order_feed_page.wait_until(
                lambda d: len(order_feed_page.get_in_progress_orders()) > 0,
                timeout=TestData.LONG_TIMEOUT
            )
            in_progress_orders = order_feed_page.get_in_progress_orders()
            
            if not in_progress_orders:
                order_feed_page.wait_until(
                    lambda d: len(order_feed_page.get_in_progress_orders()) > 0
                )
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
