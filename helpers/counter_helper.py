from selenium.webdriver.support.ui import WebDriverWait
from data.test_data import TestData


def wait_for_counter_increase(order_feed_page, counter_type, initial_value, timeout=None):
    wait = WebDriverWait(order_feed_page.driver, timeout or TestData.DEFAULT_TIMEOUT)
    
    if counter_type == "all_time":
        get_counter = order_feed_page.get_done_all_time_counter
    elif counter_type == "today":
        get_counter = order_feed_page.get_done_today_counter
    else:
        raise ValueError(f"Неизвестный тип счётчика: {counter_type}")
    
    def counter_increased(driver):
        current_counter = get_counter()
        current_value = int(current_counter) if current_counter and current_counter.isdigit() else 0
        return current_value > initial_value
    
    wait.until(counter_increased)
    
    new_counter = get_counter()
    new_value = int(new_counter) if new_counter and new_counter.isdigit() else 0
    return new_value

