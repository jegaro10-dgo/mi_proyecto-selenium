import pytest
from faker import Faker
from selenium import webdriver
from pages.purchase_page import PurchasePage

@pytest.fixture(scope="module")
def setup_teardown():
    """
    Fixture de Pytest para inicializar y cerrar el navegador.
    """
    print("\nIniciando el navegador...")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    print("\nCerrando el navegador...")
    driver.quit()

def test_guest_checkout(setup_teardown):
    """
    Prueba el flujo completo de compra con usuario invitado.
    """
    driver = setup_teardown
    try:
        print("Iniciando la prueba de compra como usuario invitado")
        fake = Faker()
        guest_email = fake.email()

        # --- Parte 1: Flujo de compra ---
        print("Paso 1: Buscando el producto..")
        purchase_page = PurchasePage(driver)
        driver.get(purchase_page.URL)

        # Llama al nuevo método para buscar el producto
        purchase_page.add_product_by_name_and_add_to_cart("14.1-inch Laptop")
        
        # Continuar con el flujo de checkout
        print("Paso 2: Navegando al carrito de compras y procediendo al checkout.")
        # Reemplazamos el driver.get() con una espera y clic en el enlace del carrito
        wait = WebDriverWait(driver, 15)
        shopping_cart_link = wait.until(EC.element_to_be_clickable(purchase_page.SHOPPING_CART_LINK))
        shopping_cart_link.click()

        purchase_page.checkout()
        purchase_page.checkout_as_guest()

        # --- Parte 2: Llenar datos de invitado ---
        print("Paso 3: Rellenando la dirección de facturación.")
        purchase_page.fill_billing_address(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=guest_email,
            country="Mexico",
            city=fake.city(),
            address1=fake.street_address(),
            zip_code=fake.zipcode(),
            phone=fake.phone_number()
        )
        purchase_page.click_shipping_address_continue()

        # --- Parte 3: Seleccionar métodos de envío y pago ---
        print("Paso 4: Seleccionando el método de envío.")
        purchase_page.select_shipping_method()
        
        print("Paso 5: Seleccionando el método de pago.")
        purchase_page.select_payment_method()
        
        # --- Parte 4: Llenar información de pago ---
        print("Paso 6: Rellenando la información de pago.")
        purchase_page.fill_payment_info()

        # --- Parte 5: Confirmar y verificar ---
        print("Paso 7: Confirmando la orden.")
        purchase_page.confirm_order()
        
        print("Paso 8: Verificando que la orden fue exitosa.")
        purchase_page.verify_order_success()

        print("¡Prueba de checkout como usuario invitado completada con éxito!")

    except Exception as e:
        pytest.fail(f"La prueba de checkout falló. Causa: {e}")
