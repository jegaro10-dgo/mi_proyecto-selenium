import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import time
from datetime import datetime

# Importa las clases de las páginas que creaste
#from pages.registration_page import RegistrationPage
#from pages.login_page import LoginPage
from pages.purchase_page import PurchasePage

def test_guest_checkout():
    """
    Prueba el flujo completo de compra con usuario invitado.
    """
    driver = webdriver.Chrome()
    driver.get("https://demowebshop.tricentis.com")

    try:
       
        print("Iniciando la prueba de compra como usuario invitado")
        fake=Faker()
        guest_email = fake.email()
        # --- Parte 1: Flujo de compra ---
        print("Paso 1: Buscando el producto..")
        Purchase_Page = PurchasePage(driver)
        # Llama nuevo método para buscar el producto
        Purchase_Page.write_name_of_product("14.1-inch Laptop")
        
        # 1.1 Añadir producto al carrito
        print("Añadiendo producto al carrito")
        #driver.find_element(By.XPATH, "//a[text()='14.1-inch Laptop']").click()
        #driver.find_element(By.ID, "add-to-cart-button-31").click()
        Purchase_Page.add_product_to_cart()
                
        # 1.2 y siguientes... Usa el objeto de la página de compra
        Purchase_Page = PurchasePage(driver)
        
        print("Ir al carrito y checkout...")
        Purchase_Page.go_to_shopping_cart()
        Purchase_Page.checkout()
        # 2 Nuevo paso para el checkout como invitado
        Purchase_Page.checkout_as_guest()
        
        print("Rellenando la dirección de facturación...")
        #Ahora el método fill_billing_address necesita el correo electrónico
        Purchase_Page.fill_billing_address(
            first_name="Jesus",
            last_name="Garcia Rojas",
            email=guest_email,
            country="Mexico",
            #state="New York",
            city="Mexico city",
            address1="123 Test St",
            zip_code="10001",
            phone="555-555-5555"
        )
        print("Continuando a la selección del método de envío...")
        Purchase_Page.click_shipping_address_continue()
        
        print("Seleccionando método de envío...")
        Purchase_Page.select_shipping_method()
        
        print("Seleccionando método de pago...")
        Purchase_Page.select_payment_method()
        
        print("Rellenando información de tarjeta...")
        Purchase_Page.fill_payment_info()
        
        print("Confirmando orden...")
        Purchase_Page.confirm_order()
        
        print("Verificando que la orden se procesó...")
        Purchase_Page.verify_order_success()

        print("Paso 3 completado: ¡Orden procesada con éxito!")
        print("Prueba End-to-End finalizada con éxito.")
        
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_filename = f"e2e_failure_{timestamp}.png"
        driver.save_screenshot(screenshot_filename)
        pytest.fail(f"La prueba End-to-End falló. Se guardó una captura de pantalla: {screenshot_filename}. Causa: {e}")
    
    finally:
        time.sleep(5)
        driver.quit()