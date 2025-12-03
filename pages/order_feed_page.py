import allure
from pages.base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators
from selenium.common.exceptions import TimeoutException
from data.test_data import TestData


class OrderFeedPage(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = OrderFeedLocators()
    
    @allure.step("Проверить загрузку страницы ленты заказов")
    def is_page_loaded(self):
        return self.is_element_visible(self.locators.ORDER_FEED_TITLE)
    
    @allure.step("Кликнуть на заказ в ленте")
    def click_order(self, order_index=0):
        orders = self.find_elements(self.locators.ORDER_ITEMS)
        if not orders or order_index >= len(orders):
            raise ValueError(f"Заказ с индексом {order_index} не найден. Всего заказов: {len(orders)}")
        
        order = orders[order_index]
        self.execute_script("arguments[0].scrollIntoView({block: 'center'});", order)
        self.wait_until(lambda driver: orders[order_index].is_displayed(), timeout=TestData.SHORT_TIMEOUT)
        
        link = self.execute_script(
            "return arguments[0].querySelector('a.OrderHistory_link__1iNby');",
            order
        )
        self.execute_script("arguments[0].click();", link)
    
    @allure.step("Проверить видимость модального окна с деталями заказа")
    def is_order_modal_visible(self):
        modal_visible = self.is_modal_visible(self.locators.ORDER_DETAILS_MODAL, timeout=TestData.SHORT_TIMEOUT)
        order_number_visible = self.is_element_visible(self.locators.MODAL_ORDER_NUMBER, timeout=TestData.SHORT_TIMEOUT)
        return modal_visible and order_number_visible
    
    @allure.step("Закрыть модальное окно с деталями заказа")
    def close_order_modal(self):
        element = self.find_element(self.locators.MODAL_CLOSE_BUTTON)
        self.execute_script("arguments[0].click();", element)
        try:
            self.wait_for_element_to_disappear(self.locators.ORDER_DETAILS_MODAL, timeout=TestData.MODAL_TIMEOUT)
        except TimeoutException:
            pass
    
    @allure.step("Получить номера заказов из ленты")
    def get_order_numbers_from_feed(self):
        orders = self.find_elements(self.locators.ORDER_ITEMS)
        return [order.find_element(*self.locators.ORDER_NUMBER).text for order in orders]
    
    @allure.step("Получить значение счётчика 'Выполнено за всё время'")
    def get_done_all_time_counter(self):
        return self.get_text(self.locators.DONE_ALL_TIME_COUNTER)
    
    @allure.step("Получить значение счётчика 'Выполнено за сегодня'")
    def get_done_today_counter(self):
        return self.get_text(self.locators.DONE_TODAY_COUNTER)
    
    @allure.step("Получить номера заказов в разделе 'В работе'")
    def get_in_progress_orders(self):
        in_progress_section = self.find_element(self.locators.IN_PROGRESS_SECTION)
        orders = in_progress_section.find_elements(*self.locators.IN_PROGRESS_ORDERS)
        return [order.text for order in orders]
    
    @allure.step("Получить номер заказа из списка")
    def get_order_number_from_list(self, order_index=0):
        orders = self.find_elements(self.locators.ORDER_ITEMS)
        if not orders or order_index >= len(orders):
            raise ValueError(f"Заказ с индексом {order_index} не найден. Всего заказов: {len(orders)}")
        order = orders[order_index]
        return order.find_element(*self.locators.ORDER_NUMBER).text
    
    @allure.step("Получить номер заказа из модального окна")
    def get_order_number_from_modal(self):
        return self.get_text(self.locators.MODAL_ORDER_NUMBER)
    
    @allure.step("Ожидать увеличения счётчика")
    def wait_for_counter_increase(self, counter_type, initial_value, timeout=None):
        timeout = timeout or TestData.DEFAULT_TIMEOUT
        
        if counter_type == "all_time":
            get_counter = self.get_done_all_time_counter
        elif counter_type == "today":
            get_counter = self.get_done_today_counter
        else:
            raise ValueError(f"Неизвестный тип счётчика: {counter_type}")
        
        self.wait_until(
            lambda driver: (
                current_value := int(current_counter) if (current_counter := get_counter()) and current_counter.isdigit() else 0
            ) is not None and current_value > initial_value,
            timeout=timeout
        )
        
        new_counter = get_counter()
        new_value = int(new_counter) if new_counter and new_counter.isdigit() else 0
        return new_value