# tests/test_guest_checkout.py

import pytest
from pages.purchase_page import PurchasePage
from faker import Faker
from datetime import datetime

# El fixture 'driver' se asume que está definido en conftest.py
def test_guest_checkout(driver):
    """
    Prueba el flujo completo de compra con usuario invitado.
    """
    try:
        print("Iniciando la prueba de compra como usuario invitado")
        fake = Faker()
        guest_email = fake.email()

        # --- Parte 1: Flujo de compra ---
        print("Paso 1: Buscando el producto..")
        purchase_page = PurchasePage(driver)

        # Llama nuevo método para buscar el producto
        purchase_page.write_name_of_product("14.1-inch Laptop")

        # 1.1 Añadir producto al carrito
        print("Añadiendo producto al carrito")
        purchase_page.add_product_to_cart()

        # 1.2 y siguientes... Usa el objeto de la página de compra
        print("Ir al carrito y checkout...")
        purchase_page.go_to_shopping_cart()
        purchase_page.checkout()

        # 2 Nuevo paso para el checkout como invitado
        purchase_page.checkout_as_guest()

        print("Rellenando la dirección de facturación...")
        # Ahora el método fill_billing_address necesita el correo electrónico
        purchase_page.fill_billing_address(
            first_name="Jesus",
            last_name="Garcia Rojas",
            email=guest_email,
            country="Mexico",
            city="Mexico city",
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

    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_filename = f"e2e_failure_{timestamp}.png"
        driver.save_screenshot(screenshot_filename)
        pytest.fail(f"La prueba End-to-End falló. Se guardó una captura de pantalla: {screenshot_filename}. Causa: {e}")
