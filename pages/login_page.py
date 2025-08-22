from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10) # Se agregó la inicialización de wait

    # --- Localizadores de la página ---
    EMAIL_INPUT = (By.ID, "Email")
    PASSWORD_INPUT = (By.ID, "Password")
    LOGIN_BUTTON = (By.CLASS_NAME, "login-button")
    LOGGED_IN_EMAIL_LINK = (By.XPATH, "//a[contains(text(), '{email}')]")

    # --- Métodos para interactuar con la página ---
    def go_to_page(self):
        self.driver.get("https://demowebshop.tricentis.com/login")

    def login_with_credentials(self, email, password):
        self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT)).send_keys(email)
        self.wait.until(EC.presence_of_element_located(self.PASSWORD_INPUT)).send_keys(password)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()
        
    def verify_login_successful(self, email):
        login_verification_locator = (By.XPATH, self.LOGGED_IN_EMAIL_LINK[1].format(email=email))
        self.wait.until(EC.presence_of_element_located(login_verification_locator))