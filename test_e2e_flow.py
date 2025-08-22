import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import time
from datetime import datetime

def test_end_to_end_purchase_flow():
    """
    Prueba el flujo completo de compra: registro, inicio de sesión y compra.
    """
    # Inicializar el WebDriver
    driver = webdriver.Chrome()

    try:
        # --- Parte 1: Registro del usuario con Faker ---
        print("Iniciando la prueba End-to-End...")
        print("Paso 1: Registrando un nuevo usuario...")
        
        fake = Faker()
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        password = "ContrasenaSegura123!"

        driver.get("https://demowebshop.tricentis.com/register")
        wait = WebDriverWait(driver, 10)
        
        driver.find_element(By.ID, "gender-male").click()
        wait.until(EC.presence_of_element_located((By.ID, "FirstName"))).send_keys(first_name)
        wait.until(EC.presence_of_element_located((By.ID, "LastName"))).send_keys(last_name)
        wait.until(EC.presence_of_element_located((By.ID, "Email"))).send_keys(email)
        wait.until(EC.presence_of_element_located((By.ID, "Password"))).send_keys(password)
        wait.until(EC.presence_of_element_located((By.ID, "ConfirmPassword"))).send_keys(password)
        driver.find_element(By.ID, "register-button").click()
        wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "result"), "Your registration completed"))
        
        print("Paso 1 completado: Usuario registrado.")
        
        # --- Parte 2: Inicio de sesión con el nuevo usuario ---
        print("Paso 2: Iniciando sesión con el usuario recién creado...")
        
        driver.get("https://demowebshop.tricentis.com/login")
        wait.until(EC.presence_of_element_located((By.ID, "Email"))).send_keys(email)
        wait.until(EC.presence_of_element_located((By.ID, "Password"))).send_keys(password)
        driver.find_element(By.CLASS_NAME, "login-button").click()
        wait.until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{email}')]")))
        
        print("Paso 2 completado: Inicio de sesión exitoso.")
        
        # --- Parte 3: Flujo de compra ---
        print("Paso 3: Iniciando el proceso de compra...")
        
        # 3.1 Añadir producto al carrito
        driver.find_element(By.XPATH, "//a[text()='14.1-inch Laptop']").click()
        driver.find_element(By.ID, "add-to-cart-button-31").click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[text()='shopping cart']")))
        
        # 3.2 Ir al carrito y checkout
        driver.find_element(By.XPATH, "//span[text()='Shopping cart']").click()
        wait.until(EC.presence_of_element_located((By.ID, "termsofservice"))).click()
        driver.find_element(By.ID, "checkout").click()
        
        # 3.3 Rellenar datos de facturación (ya precargados por el registro)
        print("Rellenando la dirección de facturación...")
        wait.until(EC.presence_of_element_located((By.ID, "BillingNewAddress_CountryId")))
        Select(driver.find_element(By.ID, "BillingNewAddress_CountryId")).select_by_visible_text("United States")
        wait.until(EC.presence_of_element_located((By.ID, "BillingNewAddress_City"))).send_keys("New York")
        wait.until(EC.presence_of_element_located((By.ID, "BillingNewAddress_Address1"))).send_keys("123 Test St")
        wait.until(EC.presence_of_element_located((By.ID, "BillingNewAddress_ZipPostalCode"))).send_keys("10001")
        wait.until(EC.presence_of_element_located((By.ID, "BillingNewAddress_PhoneNumber"))).send_keys("555-555-5555")
        print("Haciendo clic en el botón continuar Billing")
        driver.find_element(By.XPATH, "//div[@id='billing-buttons-container']/input[@value='Continue']").click()

        print("Haciendo clic en el botón continuar Shipping")
        continue_button_shipping = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='shipping-buttons-container']//input[@value='Continue']")))
        continue_button_shipping.click()
        #driver.find_element(By.XPATH, "//div[@id='shipping-buttons-container']/input[@value='Continue']").click()

        # 3.4 Seleccionar método de envío
        wait.until(EC.presence_of_element_located((By.ID, "shippingoption_0"))).click() # Ground
        driver.find_element(By.XPATH, "//div[@id='shipping-method-buttons-container']/input[@value='Continue']").click()
        
        # 3.5 Seleccionar método de pago
        wait.until(EC.presence_of_element_located((By.ID, "paymentmethod_2"))).click() # Credit Card
        driver.find_element(By.XPATH, "//div[@id='payment-method-buttons-container']/input[@value='Continue']").click()
        
        # 3.6 Rellenar información de tarjeta de crédito (datos de prueba)
        print("Rellenar datos de tarjeta")
        wait.until(EC.presence_of_element_located((By.ID, "CardholderName"))).send_keys("Test User")
        wait.until(EC.presence_of_element_located((By.ID, "CardNumber"))).send_keys("1111222233334444")
        wait.until(EC.presence_of_element_located((By.ID, "ExpireMonth"))).send_keys("01")
        wait.until(EC.presence_of_element_located((By.ID, "ExpireYear"))).send_keys("2025")
        wait.until(EC.presence_of_element_located((By.ID, "CardCode"))).send_keys("123")
        driver.find_element(By.XPATH, "//div[@id='payment-info-buttons-container']/input[@value='Continue']").click()
        
        # 3.7 Confirmar orden
        print("Confirmando orden")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='confirm-order-buttons-container']/input[@value='Confirm']"))).click()       
        # 3.8 Verificación final de la orden
        print("Verificar orden generada")
        wait.until(EC.text_to_be_present_in_element((By.XPATH, "//div[@class='section order-completed']//strong"), "Your order has been successfully processed!"))
        
        print("Paso 3 completado: ¡Orden procesada con éxito!")
        print("Prueba End-to-End finalizada con éxito.")
        
    except Exception as e:
        # Si algo falla, toma una captura de pantalla y reporta el error
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_filename = f"e2e_failure_{timestamp}.png"
        driver.save_screenshot(screenshot_filename)
        pytest.fail(f"La prueba End-to-End falló. Se guardó una captura de pantalla: {screenshot_filename}. Causa: {e}")
    
    finally:
        # Cerrar el navegador al finalizar
        time.sleep(5) # Pausa para que puedas ver el resultado
        driver.quit()