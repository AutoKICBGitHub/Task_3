import allure
from pages.base_page import BasePage
from locators.auth_locators import RestorePasswordLocators


class RestorePasswordPage(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = RestorePasswordLocators()
    
    @allure.step("Ввести email для восстановления пароля")
    def enter_email(self, email):
        self.send_keys(self.locators.EMAIL_INPUT, email)
    
    @allure.step("Кликнуть на кнопку 'Восстановить'")
    def click_restore_button(self):
        self.click_element(self.locators.RESTORE_BUTTON)
    
    @allure.step("Кликнуть на кнопку показать/скрыть пароль")
    def click_show_password_button(self):
        self.click_element(self.locators.SHOW_PASSWORD_BUTTON)
    
    @allure.step("Проверить активность поля пароля")
    def is_password_input_active(self):
        return self.is_element_active(self.locators.PASSWORD_INPUT)
    
    @allure.step("Восстановить пароль")
    def restore_password(self, email):
        self.enter_email(email)
        self.click_restore_button()
    
    @allure.step("Кликнуть на ссылку 'Войти'")
    def click_login_link(self):
        self.click_element(self.locators.LOGIN_LINK)
