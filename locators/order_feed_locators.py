from selenium.webdriver.common.by import By


class OrderFeedLocators:
    
    ORDER_FEED_TITLE = (By.XPATH, "//h1[contains(@class, 'text_type_main-large') and text()='Лента заказов']")
    ORDER_ITEMS = (By.XPATH, "//li[contains(@class, 'OrderHistory_listItem__2x95r')]")
    ORDER_NUMBER = (By.XPATH, ".//p[contains(@class, 'text_type_digits-default')]")
    ORDER_DETAILS_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_orderBox__1xWdi')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    MODAL_ORDER_NUMBER = (By.XPATH, "//p[contains(@class, 'text_type_digits-default') and contains(@class, 'mb-10') and contains(@class, 'mt-5')]")
    DONE_ALL_TIME_COUNTER = (By.XPATH, "//p[contains(text(), 'Выполнено за все время')]/following-sibling::p[contains(@class, 'OrderFeed_number__2MbrQ')]")
    DONE_TODAY_COUNTER = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p[contains(@class, 'OrderFeed_number__2MbrQ')]")
    READY_ORDERS_LIST = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderList__cBvyi') and not(contains(@class, 'OrderFeed_orderListReady__1YFem'))]")
    READY_ORDERS = (By.XPATH, ".//li[contains(@class, 'text_type_digits-default')]")
    IN_PROGRESS_SECTION = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady__1YFem')]")
    IN_PROGRESS_ORDERS = (By.XPATH, ".//li[contains(@class, 'text_type_digits-default')]")
