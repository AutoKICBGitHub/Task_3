import allure
from pages.base_page import BasePage
from locators.personal_account_locators import PersonalAccountLocators


class PersonalAccountPage(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = PersonalAccountLocators()
    
    @allure.step("Кликнуть на кнопку 'История заказов'")
    def click_order_history_button(self):
        self.click_element(self.locators.ORDER_HISTORY_BUTTON)
    
    @allure.step("Кликнуть на кнопку 'Выход'")
    def click_logout_button(self):
        self.click_element(self.locators.LOGOUT_BUTTON)
    
    @allure.step("Кликнуть на кнопку 'Профиль'")
    def click_profile_button(self):
        self.click_element(self.locators.PROFILE_BUTTON)
    
    @allure.step("Получить номера заказов из истории")
    def get_order_numbers_from_history(self):
        orders = self.find_elements(self.locators.ORDER_ITEMS)
        return [order.find_element(*self.locators.ORDER_NUMBER).text for order in orders]
    
    @allure.step("Проверить видимость истории заказов")
    def is_order_history_visible(self):
        return self.is_element_visible(self.locators.ORDER_HISTORY_BUTTON)
