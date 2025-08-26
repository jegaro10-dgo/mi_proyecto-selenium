# pages/purchase_page.py

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException


class PurchasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)  # Aumenta el tiempo de espera a 15 segundos
        self.URL = "https://demowebshop.tricentis.com"
        
        # Locators
        self.SHOPPING_CART_LINK = (By.XPATH, "//span[text()='Shopping cart']")
        self.TERMS_OF_SERVICE_CHECKBOX = (By.ID, "termsofservice")
        self.CHECKOUT_BUTTON = (By.ID, "checkout")
        self.CHECKOUT_AS_GUEST_BUTTON = (By.CSS_SELECTOR, ".checkout-as-guest-button")
        
        # New locators for product search and add to cart
        self.SEARCH_INPUT = (By.ID, "small-searchterms")
        self.SEARCH_BUTTON = (By.CSS_SELECTOR, ".search-box-button")
        self.ADD_TO_CART_BUTTON = (By.ID, "add-to-cart-button-31")

        # Billing address locators
        self.BILLING_FIRST_NAME_INPUT = (By.ID, "BillingNewAddress_FirstName")
        self.BILLING_LAST_NAME_INPUT = (By.ID, "BillingNewAddress_LastName")
        self.BILLING_EMAIL_INPUT = (By.ID, "BillingNewAddress_Email")
        self.BILLING_COUNTRY_SELECT = (By.ID, "BillingNewAddress_CountryId")
        self.BILLING_CITY_INPUT = (By.ID, "BillingNewAddress_City")
        self.BILLING_ADDRESS1_INPUT = (By.ID, "BillingNewAddress_Address1")
        self.BILLING_ZIP_CODE_INPUT = (By.ID, "BillingNewAddress_ZipPostalCode")
        self.BILLING_PHONE_INPUT = (By.ID, "BillingNewAddress_PhoneNumber")
        self.BILLING_CONTINUE_BUTTON = (By.CSS_SELECTOR, "#billing-buttons-container .new-address-next-step-button")
        
        # Shipping method locators
        self.SHIPPING_METHOD_RADIO = (By.ID, "shippingoption_0")
        self.SHIPPING_METHOD_CONTINUE_BUTTON = (By.CSS_SELECTOR, "#shipping-method-buttons-container .shipping-method-next-step-button")
        
        # Payment method locators
        self.PAYMENT_METHOD_RADIO = (By.ID, "paymentmethod_1")
        self.PAYMENT_METHOD_CONTINUE_BUTTON = (By.CSS_SELECTOR, "#payment-method-buttons-container .payment-method-next-step-button")
        
        # Payment info locators
        self.CARD_HOLDER_NAME = (By.ID, "CardholderName")
        self.CARD_NUMBER = (By.ID, "CardNumber")
        self.CARD_EXP_MONTH = (By.ID, "ExpireMonth")
        self.CARD_EXP_YEAR = (By.ID, "ExpireYear")
        self.CARD_CODE = (By.ID, "CardCode")
        self.PAYMENT_INFO_CONTINUE_BUTTON = (By.CSS_SELECTOR, "#payment-info-buttons-container .payment-info-next-step-button")
        
        # Confirmation locators
        self.CONFIRM_BUTTON = (By.CSS_SELECTOR, "#confirm-order-buttons-container .confirm-order-next-step-button")
        
        # Order success locators
        self.ORDER_SUCCESS_MESSAGE = (By.XPATH, "//div[contains(text(), 'Your order has been successfully processed!')]")
        self.ORDER_NUMBER_LINK = (By.XPATH, "//a[contains(text(), 'Click here for order details.')]")

    def go_to_shopping_cart(self):
        """
        Navega al carrito de compras.
        """
        try:
            self.driver.get(f"{self.URL}/cart")
            print("Navegado al carrito de compras.")
        except WebDriverException as e:
            pytest.fail(f"WebDriverError al navegar al carrito. Causa: {e}")
    
    def checkout(self):
        """
        Acepta los términos de servicio y hace clic en el botón de checkout.
        """
        try:
            # Esperar a que la URL del carrito se cargue correctamente
            self.wait.until(EC.url_contains("/cart"))
            
            # 1. Esperar a que el checkbox sea visible y clicable
            print("Esperando que el checkbox de términos de servicio sea clicable.")
            terms_checkbox = self.wait.until(EC.element_to_be_clickable(self.TERMS_OF_SERVICE_CHECKBOX))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", terms_checkbox)
            
            # 2. Hacer clic en el checkbox
            print("Haciendo clic en el checkbox de términos de servicio.")
            terms_checkbox.click()
            
            # 3. Hacer clic en el botón de checkout
            print("Haciendo clic en el botón de checkout.")
            self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON)).click()
        except TimeoutException as e:
            pytest.fail(f"Error de Timeout en el checkout. No se pudo interactuar con los elementos. Causa: {e}")
        except Exception as e:
            pytest.fail(f"Ocurrió un error inesperado durante el checkout. Causa: {e}")

    def checkout_as_guest(self):
        """
        Hace clic en la opción de checkout como invitado.
        """
        try:
            print("Seleccionando la opción de checkout como invitado.")
            self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_AS_GUEST_BUTTON)).click()
        except TimeoutException as e:
            pytest.fail(f"Error de Timeout en 'checkout_as_guest'. No se pudo encontrar o hacer clic en el botón 'Checkout as Guest'. Causa: {e}")

    def fill_billing_address(self, first_name, last_name, email, country, city, address1, zip_code, phone):
        """
        Rellena la dirección de facturación.
        """
        try:
            print("Rellenando la dirección de facturación.")
            # Esperar a que el formulario sea visible
            self.wait.until(EC.presence_of_element_located(self.BILLING_FIRST_NAME_INPUT))
            
            self.driver.find_element(*self.BILLING_FIRST_NAME_INPUT).send_keys(first_name)
            self.driver.find_element(*self.BILLING_LAST_NAME_INPUT).send_keys(last_name)
            self.driver.find_element(*self.BILLING_EMAIL_INPUT).send_keys(email)
            
            # Selección de país
            country_select = Select(self.driver.find_element(*self.BILLING_COUNTRY_SELECT))
            country_select.select_by_visible_text(country)
            
            self.driver.find_element(*self.BILLING_CITY_INPUT).send_keys(city)
            self.driver.find_element(*self.BILLING_ADDRESS1_INPUT).send_keys(address1)
            self.driver.find_element(*self.BILLING_ZIP_CODE_INPUT).send_keys(zip_code)
            self.driver.find_element(*self.BILLING_PHONE_INPUT).send_keys(phone)
        except (NoSuchElementException, TimeoutException) as e:
            pytest.fail(f"Error al rellenar la dirección de facturación. Un elemento no fue encontrado o la espera falló. Causa: {e}")

    def click_shipping_address_continue(self):
        """
        Hace clic en el botón de continuar en la dirección de facturación.
        """
        try:
            print("Haciendo clic en continuar de la dirección de facturación.")
            self.wait.until(EC.element_to_be_clickable(self.BILLING_CONTINUE_BUTTON)).click()
        except TimeoutException as e:
            pytest.fail(f"Error de Timeout al hacer clic en 'Continue' en la dirección de facturación. Causa: {e}")

    def select_shipping_method(self):
        """
        Selecciona el método de envío.
        """
        try:
            print("Seleccionando el método de envío.")
            self.wait.until(EC.element_to_be_clickable(self.SHIPPING_METHOD_RADIO)).click()
            self.wait.until(EC.element_to_be_clickable(self.SHIPPING_METHOD_CONTINUE_BUTTON)).click()
        except TimeoutException as e:
            pytest.fail(f"Error de Timeout al seleccionar el método de envío. Causa: {e}")

    def select_payment_method(self):
        """
        Selecciona el método de pago.
        """
        try:
            print("Seleccionando el método de pago.")
            self.wait.until(EC.element_to_be_clickable(self.PAYMENT_METHOD_RADIO)).click()
            self.wait.until(EC.element_to_be_clickable(self.PAYMENT_METHOD_CONTINUE_BUTTON)).click()
        except TimeoutException as e:
            pytest.fail(f"Error de Timeout al seleccionar el método de pago. Causa: {e}")

    def fill_payment_info(self):
        """
        Rellena la información del pago.
        """
        try:
            print("Rellenando la información de la tarjeta.")
            self.wait.until(EC.presence_of_element_located(self.CARD_HOLDER_NAME)).send_keys("Jesus Garcia Rojas")
            self.driver.find_element(*self.CARD_NUMBER).send_keys("5429999999999999")
            
            card_exp_month = Select(self.driver.find_element(*self.CARD_EXP_MONTH))
            card_exp_month.select_by_value("4")
            
            card_exp_year = Select(self.driver.find_element(*self.CARD_EXP_YEAR))
            card_exp_year.select_by_value("2026")
            
            self.driver.find_element(*self.CARD_CODE).send_keys("123")
            
            self.wait.until(EC.element_to_be_clickable(self.PAYMENT_INFO_CONTINUE_BUTTON)).click()
        except (NoSuchElementException, TimeoutException) as e:
            pytest.fail(f"Error al rellenar la información de pago. Causa: {e}")

    def confirm_order(self):
        """
        Confirma la orden.
        """
        try:
            print("Confirmando la orden.")
            self.wait.until(EC.element_to_be_clickable(self.CONFIRM_BUTTON)).click()
        except TimeoutException as e:
            pytest.fail(f"Error de Timeout al confirmar la orden. Causa: {e}")
        except WebDriverException as e:
            pytest.fail(f"Error de WebDriver al confirmar la orden. Causa: {e}")
            
    def verify_order_success(self):
        """
        Verifica que la orden fue procesada exitosamente.
        """
        try:
            print("Verificando que la orden se procesó correctamente.")
            self.wait.until(EC.presence_of_element_located(self.ORDER_SUCCESS_MESSAGE))
        except TimeoutException as e:
            pytest.fail(f"Error de Timeout al verificar el mensaje de éxito. Causa: {e}")
    
    def write_name_of_product(self, product_name):
        """
        Busca un producto por su nombre.
        """
        try:
            print(f"Buscando el producto: {product_name}")
            self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUT)).send_keys(product_name)
            self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON)).click()
        except (NoSuchElementException, TimeoutException) as e:
            pytest.fail(f"Error al buscar el producto '{product_name}'. Un elemento no fue encontrado o la espera falló. Causa: {e}")

    def add_product_to_cart(self):
        """
        Hace clic en el enlace del producto y luego en el botón de añadir al carrito.
        """
        try:
            print("Haciendo clic en el producto...")
            # El producto tiene un enlace con el texto que contiene el nombre, por lo que usaremos ese localizador
            product_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='14.1-inch Laptop']")))
            product_link.click()
            
            print("Haciendo clic en el botón 'Add to cart'...")
            self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON)).click()
        except (NoSuchElementException, TimeoutException) as e:
            pytest.fail(f"Error al añadir el producto al carrito. No se encontró el enlace o el botón. Causa: {e}")
