from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegistrationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10) # Se agregó la inicialización de wait

    # --- Localizadores de la página ---
    GENDER_MALE_RADIO = (By.ID, "gender-male")
    FIRST_NAME_INPUT = (By.ID, "FirstName")
    LAST_NAME_INPUT = (By.ID, "LastName")
    EMAIL_INPUT = (By.ID, "Email")
    PASSWORD_INPUT = (By.ID, "Password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "ConfirmPassword")
    REGISTER_BUTTON = (By.ID, "register-button")
    REGISTRATION_RESULT_TEXT = (By.CLASS_NAME, "result")

    # --- Métodos para interactuar con la página ---
    def go_to_page(self):
        self.driver.get("https://demowebshop.tricentis.com/register")

    def register_user(self, first_name, last_name, email, password):
        self.driver.find_element(*self.GENDER_MALE_RADIO).click()
        self.wait.until(EC.presence_of_element_located(self.FIRST_NAME_INPUT)).send_keys(first_name)
        self.wait.until(EC.presence_of_element_located(self.LAST_NAME_INPUT)).send_keys(last_name)
        self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT)).send_keys(email)
        self.wait.until(EC.presence_of_element_located(self.PASSWORD_INPUT)).send_keys(password)
        self.wait.until(EC.presence_of_element_located(self.CONFIRM_PASSWORD_INPUT)).send_keys(password)
        self.driver.find_element(*self.REGISTER_BUTTON).click()

    def get_registration_result(self):
        return self.wait.until(EC.text_to_be_present_in_element(self.REGISTRATION_RESULT_TEXT, "Your registration completed"))