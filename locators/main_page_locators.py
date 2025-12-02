from selenium.webdriver.common.by import By


class MainPageLocators:
    
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[contains(text(), 'Конструктор')]")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[contains(text(), 'Лента') or contains(text(), 'Заказов')]")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//p[contains(text(), 'Личный') or contains(text(), 'Кабинет')]")
    INGREDIENT_BUN = (By.XPATH, "//p[@class='BurgerIngredient_ingredient__text__yp3dH' and text()='Краторная булка N-200i']")
    INGREDIENT_SAUCE = (By.XPATH, "//p[@class='BurgerIngredient_ingredient__text__yp3dH' and text()='Соус Spicy-X']")
    INGREDIENT_MAIN = (By.XPATH, "//p[@class='BurgerIngredient_ingredient__text__yp3dH' and text()='Мясо бессмертных моллюсков Protostomia']")
    INGREDIENT_DETAILS_MODAL = (By.XPATH, "//section[contains(@class, 'Modal_modal__P3_V5')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    MODAL_TITLE = (By.XPATH, "//h2[contains(@class, 'text_type_main-large')]")
    CONSTRUCTOR_DROP_AREA = (By.XPATH, "//ul[contains(@class, 'BurgerConstructor_basket__list__l9dp_')]")
    ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ') or contains(text(), 'Войти в аккаунт')]")
    INGREDIENT_COUNTER = (By.XPATH, ".//p[@class='counter_counter__num__3nue1']")
    INGREDIENT_COUNTER_CONTAINER = (By.XPATH, ".//div[contains(@class, 'counter_counter__ZNLkj')]")
    ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'text_type_digits-large')]")
    ORDER_MODAL = (By.XPATH, "//section[contains(@class, 'Modal_modal__P3_V5')]//h2[contains(@class, 'text_type_digits-large')]")
    ORDER_MODAL_OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay__x2ZCr')]")
