from selenium.webdriver.common.by import By


class PersonalAccountLocators:
    
    PROFILE_BUTTON = (By.XPATH, "//a[contains(@class, 'Account_link__2ETsJ') and text()='Профиль']")
    ORDER_HISTORY_BUTTON = (By.XPATH, "//a[contains(@class, 'Account_link__2ETsJ') and text()='История заказов']")
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(@class, 'Account_button__14Yp3') and text()='Выход']")
    NAME_INPUT = (By.XPATH, "//input[@name='Name' and contains(@class, 'input__textfield')]")
    EMAIL_INPUT = (By.XPATH, "//input[@name='name' and contains(@class, 'input__textfield') and @type='text']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password' and contains(@class, 'input__textfield')]")
    ORDER_ITEMS = (By.XPATH, "//li[contains(@class, 'OrderHistory_listItem__2x95r')]")
    ORDER_NUMBER = (By.XPATH, ".//p[contains(@class, 'text_type_digits-default')]")
