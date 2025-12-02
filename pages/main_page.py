import allure
from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators
from selenium.webdriver.common.by import By
from data.test_data import TestData


class MainPage(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = MainPageLocators()
    
    @allure.step("Кликнуть на кнопку 'Конструктор'")
    def click_constructor_button(self):
        self._close_any_modal_if_present()
        self.click_element(self.locators.CONSTRUCTOR_BUTTON)
    
    @allure.step("Кликнуть на кнопку 'Лента заказов'")
    def click_order_feed_button(self):
        self._close_any_modal_if_present()
        self.click_element(self.locators.ORDER_FEED_BUTTON)
    
    @allure.step("Кликнуть на кнопку 'Личный кабинет'")
    def click_personal_account_button(self):
        self._close_any_modal_if_present()
        self.click_element(self.locators.PERSONAL_ACCOUNT_BUTTON)
    
    @allure.step("Кликнуть на ингредиент")
    def click_ingredient(self, ingredient_locator):
        self.click_element(ingredient_locator)
    
    @allure.step("Проверить видимость модального окна с деталями ингредиента")
    def is_ingredient_modal_visible(self):
        return self.is_modal_visible(self.locators.INGREDIENT_DETAILS_MODAL, timeout=TestData.MODAL_TIMEOUT)
    
    @allure.step("Закрыть модальное окно с деталями ингредиента")
    def close_ingredient_modal(self):
        self.close_modal(
            self.locators.MODAL_CLOSE_BUTTON,
            self.locators.INGREDIENT_DETAILS_MODAL
        )
    
    @allure.step("Получить значение счётчика ингредиента")
    def get_ingredient_counter(self, ingredient_locator):
        element = self.find_element(ingredient_locator)
        parent = element.find_element(By.XPATH, "./ancestor::a[contains(@class, 'BurgerIngredient_ingredient__1TVf6')]")
        counter_element = parent.find_element(*self.locators.INGREDIENT_COUNTER)
        counter_text = counter_element.text.strip()
        return int(counter_text) if counter_text and counter_text.isdigit() else 0
    
    @allure.step("Добавить ингредиент в конструктор")
    def add_ingredient_to_constructor(self, ingredient_locator):
        ingredient_text = self.find_element(ingredient_locator)
        ingredient = ingredient_text.find_element(By.XPATH, "./ancestor::a[contains(@class, 'BurgerIngredient_ingredient__1TVf6')]")
        drop_area = self.find_element(self.locators.CONSTRUCTOR_DROP_AREA)
        
        self.driver.execute_script("""
            var source = arguments[0];
            var target = arguments[1];
            var dragStartEvent = new DragEvent('dragstart', {
                bubbles: true,
                cancelable: true,
                dataTransfer: new DataTransfer()
            });
            source.dispatchEvent(dragStartEvent);
            var dragOverEvent = new DragEvent('dragover', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dragStartEvent.dataTransfer
            });
            target.dispatchEvent(dragOverEvent);
            var dropEvent = new DragEvent('drop', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dragStartEvent.dataTransfer
            });
            target.dispatchEvent(dropEvent);
        """, ingredient, drop_area)
    
    @allure.step("Кликнуть на кнопку 'Оформить заказ'")
    def click_order_button(self):
        self.click_element(self.locators.ORDER_BUTTON)
    
    @allure.step("Получить номер заказа из модального окна")
    def get_order_number(self):
        self.wait_for_element_visible(self.locators.ORDER_NUMBER, timeout=TestData.DEFAULT_TIMEOUT)
        order_number = self.get_text(self.locators.ORDER_NUMBER)
        return order_number.strip() if order_number and order_number.strip() else ""
    
    @allure.step("Проверить видимость модального окна с номером заказа")
    def is_order_modal_visible(self):
        modal_visible = self.is_modal_visible(self.locators.INGREDIENT_DETAILS_MODAL, timeout=TestData.SHORT_TIMEOUT)
        order_number_visible = self.is_element_visible(self.locators.ORDER_NUMBER, timeout=TestData.SHORT_TIMEOUT)
        return modal_visible and order_number_visible
    
    @allure.step("Закрыть модальное окно с номером заказа")
    def close_order_modal(self):
        self.close_modal(
            self.locators.MODAL_CLOSE_BUTTON,
            self.locators.INGREDIENT_DETAILS_MODAL
        )
    
    def _close_any_modal_if_present(self):
        if self.is_modal_visible(self.locators.INGREDIENT_DETAILS_MODAL, timeout=TestData.VERY_SHORT_TIMEOUT):
            self.close_order_modal()
