import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.purchase_page import PurchasePage  # Importamos la clase de página refactorizada

@pytest.fixture(scope="module")
def setup_teardown():
    """
    Fixture de Pytest para inicializar y cerrar el navegador.
    Utiliza el patrón de Page Object Model.
    """
    print("\nIniciando el navegador...")
    # Usa webdriver_manager para gestionar automáticamente el driver de Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    print("\nCerrando el navegador...")
    driver.quit()

def test_end_to_end_purchase_flow(setup_teardown):
    """
    Prueba de extremo a extremo del flujo de compra como usuario invitado.
    Utiliza la clase PurchasePage para interactuar con la web.
    """
    driver = setup_teardown
    purchase_page = PurchasePage(driver)
    
    # Paso 1: Navegar a la página de inicio
    print("Navegando a la página de inicio...")
    driver.get(purchase_page.URL)

    # Paso 2: Buscar un producto y agregarlo al carrito.
    # Usamos el nuevo método combinado para mayor robustez.
    print("Paso 2: Buscando y agregando el producto '14.1-inch Laptop' al carrito.")
    purchase_page.add_product_by_name_and_add_to_cart("14.1-inch Laptop")
    
    # Paso 3: Navegar al carrito y proceder al checkout
    print("Paso 3: Navegando al carrito de compras y procediendo al checkout.")
    purchase_page.go_to_shopping_cart()
    purchase_page.checkout()
    purchase_page.checkout_as_guest()

    # Paso 4: Rellenar la dirección de facturación
    print("Paso 4: Rellenando la dirección de facturación.")
    purchase_page.fill_billing_address(
        first_name="NombrePrueba",
        last_name="ApellidoPrueba",
        email="prueba@prueba.com",
        country="Mexico",
        city="Ciudad de Mexico",
        address1="Calle Falsa 123",
        zip_code="01000",
        phone="5512345678"
    )
    purchase_page.click_shipping_address_continue()

    # Paso 5: Seleccionar el método de envío
    print("Paso 5: Seleccionando el método de envío.")
    purchase_page.select_shipping_method()

    # Paso 6: Seleccionar el método de pago
    print("Paso 6: Seleccionando el método de pago.")
    purchase_page.select_payment_method()

    # Paso 7: Rellenar la información de pago
    print("Paso 7: Rellenando la información de pago.")
    purchase_page.fill_payment_info()

    # Paso 8: Confirmar la orden
    print("Paso 8: Confirmando la orden.")
    purchase_page.confirm_order()

    # Paso 9: Verificar el mensaje de éxito
    print("Paso 9: Verificando que la orden se procesó correctamente.")
    purchase_page.verify_order_success()

    print("\n¡Prueba de flujo de compra completada con éxito!")

