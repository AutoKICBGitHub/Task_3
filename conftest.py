import pytest
import allure
import os
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.auth_page import AuthPage
from pages.restore_password_page import RestorePasswordPage
from pages.personal_account_page import PersonalAccountPage
from pages.order_feed_page import OrderFeedPage
from helpers.api_helper import ApiHelper
from data.test_data import TestData


@pytest.fixture(scope="function")
def driver_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    try:
        driver_path = ChromeDriverManager().install()
        
        if os.name == 'nt' and not driver_path.endswith('.exe'):
            driver_dir = os.path.dirname(driver_path)
            exe_path = os.path.join(driver_dir, 'chromedriver.exe')
            if os.path.exists(exe_path):
                driver_path = exe_path
        
        service = ChromeService(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(TestData.IMPLICIT_WAIT)
        driver.maximize_window()
        
        yield driver
        
        driver.quit()
        
    except Exception as e:
        pytest.skip(f"Не удалось запустить Chrome: {e}")


@pytest.fixture(scope="function")
def driver_firefox():
    options = webdriver.FirefoxOptions()
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    
    try:
        cache_dir = os.path.join(os.path.expanduser("~"), ".wdm", "drivers", "geckodriver")
        if not os.path.exists(cache_dir):
            pytest.skip("Firefox драйвер не найден в кэше. Превышен лимит запросов к GitHub API.")
        
        driver_path = GeckoDriverManager().install()
        
        if not os.path.exists(driver_path):
            pytest.skip(f"GeckoDriver не найден по пути: {driver_path}")
        
        service = FirefoxService(driver_path)
        driver = webdriver.Firefox(service=service, options=options)
        driver.implicitly_wait(TestData.IMPLICIT_WAIT)
        driver.maximize_window()
        
        yield driver
        
        driver.quit()
        
    except ValueError as e:
        if "rate limit" in str(e).lower() or "API rate limit" in str(e):
            pytest.skip("Превышен лимит запросов к GitHub API для Firefox драйвера.")
        else:
            pytest.skip(f"Ошибка при загрузке Firefox драйвера: {e}")
    except Exception as e:
        pytest.skip(f"Не удалось запустить Firefox: {e}")


@pytest.fixture(scope="function")
def driver(request):
    chrome_marker = request.node.get_closest_marker("chrome")
    firefox_marker = request.node.get_closest_marker("firefox")
    
    if chrome_marker:
        driver_instance = request.getfixturevalue("driver_chrome")
    elif firefox_marker:
        driver_instance = request.getfixturevalue("driver_firefox")
    else:
        driver_instance = request.getfixturevalue("driver_chrome")
    
    yield driver_instance


def generate_test_email():
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_string}@example.com"


@pytest.fixture(scope="function")
def test_user():
    api = ApiHelper()
    email = generate_test_email()
    password = "test_password_123"
    name = "Test User"
    
    token = api.create_user_and_get_token(email, password, name)
    
    yield {
        "email": email,
        "password": password,
        "name": name,
        "token": token
    }
    
    if token:
        api.delete_user(token)


@pytest.fixture(scope="function")
def logged_in_user(driver, test_user):
    driver.get(TestData.BASE_URL)
    
    main_page = MainPage(driver)
    main_page.click_personal_account_button()
    
    wait = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
    wait.until(EC.url_contains("login"))
    
    auth_page = AuthPage(driver)
    auth_page.login(test_user["email"], test_user["password"])
    
    wait.until(EC.url_to_be(TestData.BASE_URL))
    
    yield test_user


@pytest.fixture(scope="function")
def main_page(driver):
    driver.get(TestData.BASE_URL)
    return MainPage(driver)


@pytest.fixture(scope="function")
def auth_page(driver):
    driver.get(f"{TestData.BASE_URL}login")
    return AuthPage(driver)


@pytest.fixture(scope="function")
def restore_password_page(driver):
    driver.get(f"{TestData.BASE_URL}forgot-password")
    return RestorePasswordPage(driver)


@pytest.fixture(scope="function")
def personal_account_page(driver, logged_in_user):
    driver.get(TestData.BASE_URL)
    main_page = MainPage(driver)
    main_page.click_personal_account_button()
    
    wait = WebDriverWait(driver, TestData.DEFAULT_TIMEOUT)
    wait.until(EC.url_contains("account"))
    
    return PersonalAccountPage(driver)


@pytest.fixture(scope="function")
def order_feed_page(driver):
    driver.get(f"{TestData.BASE_URL}feed")
    return OrderFeedPage(driver)


@pytest.fixture(scope="function")
def created_order(driver, logged_in_user):
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
    
    wait_long = WebDriverWait(driver, TestData.ORDER_MODAL_TIMEOUT)
    
    def order_number_visible(driver):
        return main_page.is_element_visible(main_page.locators.ORDER_NUMBER, timeout=TestData.SHORT_TIMEOUT)
    
    wait_long.until(order_number_visible)
    
    def order_number_valid(driver):
        order_num = main_page.get_order_number()
        return order_num and order_num.strip() and order_num.strip() != "9999" and order_num.strip() != ""
    
    wait_long.until(order_number_valid)
    order_number = main_page.get_order_number()
    assert order_number and order_number.strip() and order_number.strip() != "9999", \
        f"Не удалось получить номер заказа. Получено: {order_number}"
    main_page.close_order_modal()
    
    return order_number


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        if "driver" in item.funcargs:
            driver = item.funcargs["driver"]
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass
