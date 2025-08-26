from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pytest

class PurchasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10) # Se agregó la inicialización de wait

    # Localizadores para la búsqueda del producto
    WRITE_NAME = (By.ID, "small-searchterms")
    SEARCH = (By.XPATH, "//input[@value='Search']")

    # Localizadores para la página de la laptop
    LAPTOP_LINK = (By.XPATH, "//a[text()='14.1-inch Laptop']")
    ADD_TO_CART_BUTTON = (By.XPATH, "//input[@value='Add to cart']")

    # --- Localizadores de la página ---
    SHOPPING_CART_LINK = (By.XPATH, "//span[text()='Shopping cart']")
    TERMS_OF_SERVICE_CHECKBOX = (By.ID, "termsofservice")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    GUEST_CHECKOUT_BUTTON = (By.XPATH, "//input[@value='Checkout as Guest']")
    
    # Localizadores de la página de facturación
    BILLING_FIRST_NAME = (By.ID, "BillingNewAddress_FirstName")
    BILLING_LAST_NAME = (By.ID, "BillingNewAddress_LastName")
    BILLING_EMAIL_INPUT = (By.ID, "BillingNewAddress_Email")
    BILLING_COUNTRY_DROPDOWN = (By.ID, "BillingNewAddress_CountryId")
    #BILLING_STATE_DROPDOWN = (By.ID, "BillingNewAddress_StateProvinceId")
    BILLING_CITY_INPUT = (By.ID, "BillingNewAddress_City")
    BILLING_ADDRESS1_INPUT = (By.ID, "BillingNewAddress_Address1")
    BILLING_ZIP_INPUT = (By.ID, "BillingNewAddress_ZipPostalCode")
    BILLING_PHONE_INPUT = (By.ID, "BillingNewAddress_PhoneNumber")
    BILLING_CONTINUE_BUTTON = (By.XPATH, "//div[@id='billing-buttons-container']/input[@value='Continue']")

    # Localizadores de la página de dirección de envío
    SHIPPING_ADDRESS_CONTINUE_BUTTON = (By.XPATH, "//div[@id='shipping-buttons-container']/input[@value='Continue']")
    
    # Localizadores de la página de envío
    SHIPPING_METHOD_RADIO = (By.ID, "shippingoption_0")
    SHIPPING_CONTINUE_BUTTON = (By.XPATH, "//div[@id='shipping-method-buttons-container']/input[@value='Continue']")
    
    # Localizadores de la página de pago
    PAYMENT_METHOD_RADIO = (By.ID, "paymentmethod_2")
    PAYMENT_CONTINUE_BUTTON = (By.XPATH, "//div[@id='payment-method-buttons-container']/input[@value='Continue']")

    # Localizadores de información de tarjeta de crédito
    CARDHOLDER_NAME_INPUT = (By.ID, "CardholderName")
    CARD_NUMBER_INPUT = (By.ID, "CardNumber")
    EXPIRE_MONTH_DROPDOWN = (By.ID, "ExpireMonth")
    EXPIRE_YEAR_DROPDOWN = (By.ID, "ExpireYear")
    CARD_CODE_INPUT = (By.ID, "CardCode")
    PAYMENT_INFO_CONTINUE_BUTTON = (By.XPATH, "//div[@id='payment-info-buttons-container']/input[@value='Continue']")
    
    # Localizadores de la página de confirmación
    CONFIRM_BUTTON = (By.XPATH, "//div[@id='confirm-order-buttons-container']/input[@value='Confirm']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[@class='section order-completed']//strong")
    
    # --- Métodos para interactuar con la página ---
    def write_name_of_product(self,name_product):
        self.wait.until(EC.presence_of_element_located(self.WRITE_NAME)).send_keys(name_product)
        self.wait.until(EC.element_to_be_clickable(self.SEARCH)).click()

    def add_product_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.LAPTOP_LINK)).click()
        self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON)).click()

    def go_to_shopping_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.SHOPPING_CART_LINK)).click()

    def checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.TERMS_OF_SERVICE_CHECKBOX)).click()
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON)).click()

    def checkout_as_guest(self):
        self.wait.until(EC.element_to_be_clickable(self.GUEST_CHECKOUT_BUTTON)).click()

    def fill_billing_address(self, first_name, last_name, email, country, city, address1, zip_code, phone, state=None):
        #campos obligatorios para usuario invitado
        print("Llenando datos de usuario invitado")
        try:
            self.wait.until(EC.presence_of_element_located(self.BILLING_EMAIL_INPUT)).send_keys(email)
            self.wait.until(EC.presence_of_element_located(self.BILLING_FIRST_NAME)).send_keys(first_name)
            self.wait.until(EC.presence_of_element_located(self.BILLING_LAST_NAME)).send_keys(last_name)
            
            Select(self.wait.until(EC.presence_of_element_located(self.BILLING_COUNTRY_DROPDOWN))).select_by_visible_text(country)
            
            # Ahora, solo si se proporciona un estado, intentamos seleccionarlo.
            if state:
                self.wait.until(EC.presence_of_element_located(self.BILLING_STATE_DROPDOWN))
                Select(self.driver.find_element(*self.BILLING_STATE_DROPDOWN)).select_by_visible_text(state)

            self.driver.find_element(*self.BILLING_CITY_INPUT).send_keys(city)
            self.driver.find_element(*self.BILLING_ADDRESS1_INPUT).send_keys(address1)
            self.driver.find_element(*self.BILLING_ZIP_INPUT).send_keys(zip_code)
            self.driver.find_element(*self.BILLING_PHONE_INPUT).send_keys(phone)
            self.wait.until(EC.element_to_be_clickable(self.BILLING_CONTINUE_BUTTON)).click()
        except TimeoutException as e:
            pytest.fail(f"Error de time out al rellenar la dirección de facturación. Causa{e} ")

    def click_shipping_address_continue(self):
        self.wait.until(EC.element_to_be_clickable(self.SHIPPING_ADDRESS_CONTINUE_BUTTON)).click()

    def select_shipping_method(self):
        self.wait.until(EC.presence_of_element_located(self.SHIPPING_METHOD_RADIO)).click()
        self.wait.until(EC.element_to_be_clickable(self.SHIPPING_CONTINUE_BUTTON)).click()

    def select_payment_method(self):
        self.wait.until(EC.presence_of_element_located(self.PAYMENT_METHOD_RADIO)).click()
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_CONTINUE_BUTTON)).click()
    
    def fill_payment_info(self):
        self.wait.until(EC.presence_of_element_located(self.CARDHOLDER_NAME_INPUT)).send_keys("Test User")
        self.wait.until(EC.presence_of_element_located(self.CARD_NUMBER_INPUT)).send_keys("1111222233334444")
        self.wait.until(EC.presence_of_element_located(self.EXPIRE_MONTH_DROPDOWN)).send_keys("01")
        self.wait.until(EC.presence_of_element_located(self.EXPIRE_YEAR_DROPDOWN)).send_keys("2025")
        self.wait.until(EC.presence_of_element_located(self.CARD_CODE_INPUT)).send_keys("123")
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_INFO_CONTINUE_BUTTON)).click()
        
    def confirm_order(self):
        try:
            self.wait.until(EC.element_to_be_clickable(self.CONFIRM_BUTTON)).click()
        except TimeoutException as e:
            pytest.fail(f"Error de timeout al confirmar la orden. Causa: {e}")
    
    def verify_order_success(self):
        self.wait.until(EC.text_to_be_present_in_element(self.SUCCESS_MESSAGE, "Your order has been successfully processed!"))