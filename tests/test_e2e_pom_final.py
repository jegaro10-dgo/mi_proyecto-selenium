import pytest
from selenium.webdriver.common.by import By
from faker import Faker


# Importa las clases de las páginas que creaste
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from pages.purchase_page import PurchasePage

def test_end_to_end_purchase_flow(driver):
    """
    Prueba el flujo completo de compra: registro, inicio de sesión y compra.
    """
    # --- Parte 1: Registro del usuario con Faker ---
    print("Iniciando la prueba End-to-End...")
    print("Paso 1: Registrando un nuevo usuario...")
    
    fake = Faker()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    password = "ContrasenaSegura123!"

    # Usa el objeto de la página de registro para el flujo de registro
    registration_page = RegistrationPage(driver)
    registration_page.go_to_page()
    registration_page.register_user(first_name, last_name, email, password)
    registration_page.get_registration_result()
    
    print("Paso 1 completado: Usuario registrado.")
    
    # --- Parte 2: Inicio de sesión con el nuevo usuario ---
    print("Paso 2: Iniciando sesión con el usuario recién creado...")
    
    # Usa el objeto de la página de inicio de sesión para el flujo de login
    login_page = LoginPage(driver)
    login_page.go_to_page()
    login_page.login_with_credentials(email, password)
    login_page.verify_login_successful(email)
    
    print("Paso 2 completado: Inicio de sesión exitoso.")
    
    # --- Parte 3: Flujo de compra ---
    print("Paso 3: Iniciando el proceso de compra...")
    
    # 3.1 Añadir producto al carrito
    driver.find_element(By.XPATH, "//a[text()='14.1-inch Laptop']").click()
    driver.find_element(By.ID, "add-to-cart-button-31").click()
    
    # 3.2 y siguientes... Usa el objeto de la página de compra
    purchase_page = PurchasePage(driver)
    
    print("Ir al carrito y checkout...")
    purchase_page.go_to_shopping_cart()
    purchase_page.checkout()
    
    print("Rellenando la dirección de facturación...")
    purchase_page.fill_billing_address(
        first_name="Jesus",
        last_name="Garcia Rojas",
        email=email,
        country="Mexico",
        #state="New York",
        city="New York",
        address1="123 Test St",
        zip_code="10001",
        phone="555-555-5555"
    )
    print("Continuando a la selección del método de envío...")
    purchase_page.click_shipping_address_continue()
    
    print("Seleccionando método de envío...")
    purchase_page.select_shipping_method()
    
    print("Seleccionando método de pago...")
    purchase_page.select_payment_method()
    
    print("Rellenando información de tarjeta...")
    purchase_page.fill_payment_info()
    
    print("Confirmando orden...")
    purchase_page.confirm_order()
    
    print("Verificando que la orden se procesó...")
    purchase_page.verify_order_success()

    print("Paso 3 completado: ¡Orden procesada con éxito!")
    print("Prueba End-to-End finalizada con éxito.")
    