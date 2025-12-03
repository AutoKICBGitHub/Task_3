from selenium.webdriver.common.by import By


class AuthLocators:
    
    EMAIL_INPUT = (By.XPATH, "//label[contains(text(), 'Email')]/following-sibling::input")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='Пароль' and @type='password']")
    PASSWORD_INPUT_GENERAL = (By.XPATH, "//input[@name='Пароль']")
    NAME_INPUT = (By.XPATH, "//label[contains(text(), 'Имя')]/following-sibling::input")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(@class, 'button_button') and text()='Войти']")
    REGISTER_BUTTON = (By.XPATH, "//button[contains(@class, 'button_button') and text()='Зарегистрироваться']")
    RESTORE_PASSWORD_BUTTON = (By.XPATH, "//a[contains(@class, 'Auth_link__1fOlj') and text()='Восстановить пароль']")
    REGISTER_LINK = (By.XPATH, "//a[contains(@class, 'Auth_link__1fOlj') and text()='Зарегистрироваться']")
    LOGIN_LINK = (By.XPATH, "//a[text()='Войти']")


class RestorePasswordLocators:
    
    EMAIL_INPUT = (By.XPATH, "//label[contains(text(), 'Email')]/following-sibling::input")
    RESTORE_BUTTON = (By.XPATH, "//button[contains(@class, 'button_button') and text()='Восстановить']")
    PASSWORD_INPUT = (By.XPATH, "//label[contains(text(), 'Пароль')]/following-sibling::input[@type='password']")
    CODE_INPUT = (By.XPATH, "//label[contains(text(), 'Введите код из письма')]/following-sibling::input")
    SAVE_BUTTON = (By.XPATH, "//button[contains(@class, 'button_button') and text()='Сохранить']")
    SHOW_PASSWORD_BUTTON = (By.XPATH, "//div[contains(@class, 'input__icon') and contains(@class, 'input__icon-action')]")
    LOGIN_LINK = (By.XPATH, "//a[contains(@class, 'Auth_link__1fOlj') and text()='Войти']")
