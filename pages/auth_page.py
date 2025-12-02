import allure
from pages.base_page import BasePage
from locators.auth_locators import AuthLocators
from locators.main_page_locators import MainPageLocators


class AuthPage(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = AuthLocators()
    
    @allure.step("Ввести email")
    def enter_email(self, email):
        self.send_keys(self.locators.EMAIL_INPUT, email)
    
    @allure.step("Ввести пароль")
    def enter_password(self, password):
        self.send_keys(self.locators.PASSWORD_INPUT, password)
    
    @allure.step("Кликнуть на кнопку 'Войти'")
    def click_login_button(self):
        self.click_element(self.locators.LOGIN_BUTTON)
    
    @allure.step("Кликнуть на ссылку 'Зарегистрироваться'")
    def click_register_link(self):
        self.click_element(self.locators.REGISTER_LINK)
    
    @allure.step("Авторизоваться")
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
    
    @allure.step("Кликнуть на кнопку 'Восстановить пароль'")
    def click_restore_password_button(self):
        self.click_element(self.locators.RESTORE_PASSWORD_BUTTON)
    
    @allure.step("Кликнуть на кнопку 'Личный кабинет' в хедере")
    def click_personal_account_button(self):
        main_locators = MainPageLocators()
        self.click_element(main_locators.PERSONAL_ACCOUNT_BUTTON)
