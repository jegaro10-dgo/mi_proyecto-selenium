from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

# Datos de la cuenta de prueba
# jegaro10@MacBook-Pro-de-Jesus ~ % cd mi_prueba_selenium
#jegaro10@MacBook-Pro-de-Jesus mi_prueba_selenium % source venv/bin/activate
EMAIL = "prueba_selenium@example.com"
CONTRASENA = "ContrasenaSegura123!"

# 1. Configurar el WebDriver para Chrome
driver = webdriver.Chrome()

try:
    # 2. Navegar a la página de inicio de sesión
    print("Abriendo la página de inicio de sesión...")
    driver.get("https://demowebshop.tricentis.com/login")
    
    # 3. Rellenar los campos del formulario de inicio de sesión
    print("Rellenando el formulario de inicio de sesión...")
    wait = WebDriverWait(driver, 10)
    
    email_field = wait.until(EC.presence_of_element_located((By.ID, "Email")))
    email_field.send_keys(EMAIL)
    
    password_field = wait.until(EC.presence_of_element_located((By.ID, "Password")))
    password_field.send_keys(CONTRASENA)
    
    # 4. Hacer clic en el botón de inicio de sesión
    print("Haciendo clic en el botón de inicio de sesión...")
    driver.find_element(By.CLASS_NAME, "login-button").click()

    # 5. Verificar que el inicio de sesión fue exitoso
    print("Verificando que el inicio de sesión fue exitoso...")
    wait.until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{EMAIL}')]")))
    print("¡Inicio de sesión exitoso!")
    
    """# 6. Buscar el producto "Computing and Internet"
    print("Buscando el producto 'Computing and Internet'...")
    search_box = wait.until(EC.presence_of_element_located((By.ID, "small-searchterms")))
    search_box.send_keys("Computing and Internet")
    search_box.send_keys(Keys.RETURN)

    # 7. Hacer clic en el resultado de la búsqueda para ir a la página del producto
    print("Haciendo clic en el resultado de la búsqueda...")
    product_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Computing and Internet")))
    product_link.click()

    # 8. Añadir el producto al carrito desde la página de detalles
    print("Añadiendo el producto al carrito...")
    add_to_cart_button = wait.until(EC.presence_of_element_located((By.ID, "add-to-cart-button-13")))
    add_to_cart_button.click()
    
    # 9. Verificar que el producto se añadió
    print("Verificando que el producto se añadió al carrito...")

    # Esperamos a que el pop-up de éxito sea visible y contenga el texto.
    wait.until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "bar-notification.success"),
            "The product has been added to your shopping cart"
        )
    )
    print("¡Producto añadido, iniciando el proceso de checkout!...")"""

    # Pasos para el checkout

    # 10. Hacer clic en el enlace del carrito
    print("Navegando al carrito...")
    shopping_cart_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Shopping cart']")))
    shopping_cart_link.click()

    # 11. Aceptar los términos de servicio
    print("Aceptando los términos de servicio...")
    terms_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "termsofservice")))
    terms_checkbox.click()

    # 12. Hacer clic en el botón de Checkout
    print("Haciendo clic en el botón 'Checkout'...")
    checkout_button = wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
    checkout_button.click()

    print("¡El proceso de Checkout ha comenzado con éxito!")

    # Pasos para Billing Address

    # 13. Rellenar el formulario de la dirección de facturación solo datos obligatorios
    """print("Rellenando la dirección de facturación...")
    country_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "BillingNewAddress_CountryId"))))
    country_dropdown.select_by_visible_text("Mexico")

    # Rellenado la ciudad
    city_field = wait.until(EC.presence_of_element_located((By.ID, "BillingNewAddress_City")))
    city_field.send_keys("Ciudad de México")

    # Rellenado la dirección 1
    address1_field = wait.until(EC.presence_of_element_located((By.ID, "BillingNewAddress_Address1")))
    address1_field.send_keys("Calle falsa 123")

    # Rellenando el código postal
    zip_field = wait.until(EC.presence_of_element_located ((By.ID, "BillingNewAddress_ZipPostalCode")))
    zip_field.send_keys("01000")

    # Rellenando el número de teléfono
    phone_field = wait.until(EC.presence_of_element_located((By.ID, "BillingNewAddress_PhoneNumber")))
    phone_field.send_keys("5512345678")
    print("Dirección completada con éxito haciendo clicl en continue...")#"""

    # Haer click en el botón continue
    print("Continuando al siguiente paso de dirección de envío")
    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='Billing.save()']")))
    continue_button.click()
    print("¡Dirección de facturaciión rellenada con éxito!")

    #  14 Dar click en el botón continue de la página de dirección de envío
    continue_button_shipping = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='shipping-buttons-container']//input[@value='Continue']")))
    continue_button_shipping.click()
    print("Dirección de envío completada con éxito...")

    # 15 Seleccionar el método de envío
    print("Seleccionando el método de envío")
    shipping_method = wait.until(EC.element_to_be_clickable((By.ID, "shippingoption_2")))
    shipping_method.click()
    print("Método de envío seleccionado")
    #Hacer clic en el botón continue
    button_shipping_method = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='shipping-method-buttons-container']//input[@value='Continue']")))
    button_shipping_method.click()
    print("Método de envió completado")

    # 16 Seleccionar el método de pago
    print("Seleccionando el método de pago")
    payment_method = wait.until(EC.element_to_be_clickable((By.ID, "paymentmethod_2")))
    payment_method.click()
    print("Método de pago seleecionado")
    #Hacer clic en el botón continue
    button_payment_method = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='PaymentMethod.save()']")))
    button_payment_method.click()
    print("Método de pago seleccionado")

    # 17 Completar información de pago
    print("Seleccionar el tipo de tarjeta")
    select_card = Select(wait.until(EC.presence_of_element_located((By.ID, "CreditCardType"))))
    select_card.select_by_value("MasterCard")
    print("Agregando nombre de la tarjeta")
    card_name = wait.until(EC.presence_of_element_located((By.ID, "CardholderName")))
    card_name.send_keys("Jesus Garcia Rojas")
    print("Agregar el numero de la tarjeta de prueba")
    card_number = wait.until(EC.presence_of_element_located((By.ID, "CardNumber")))
    card_number.send_keys("4929000000000000")
    print("Seleccionando el mes de expiración")
    select_month = Select(wait.until(EC.presence_of_element_located((By.ID, "ExpireMonth"))))
    select_month.select_by_value("3")
    print("Seleccionando el año de expiración")
    select_year = Select(wait.until(EC.presence_of_element_located((By.ID, "ExpireYear"))))
    select_year.select_by_value("2030")
    print("Rellenar código cvv")
    cvv=wait.until(EC.presence_of_element_located((By.ID, "CardCode")))
    cvv.send_keys("987")
    print("Click en el botón de confirmación")
    button_confirmation  =  wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='PaymentInfo.save()']")))
    button_confirmation.click()

    # 18 Verificar que la orden se completó
    print("confirmando la orden...")
    confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@onclick='ConfirmOrder.save()']")))
    confirm_button.click()

    # 19 Confirmar que la orden se completó
    print("Confirmando que la orden se completo")
    wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Thank you')]")))
    print("ORDEN EXITOSA, EL PROCESO SE COMPLETÓ ")


except Exception as e:
    print(f"Ocurrió un error en la prueba: {e}")

finally:
    # Pausar 5 segundos para que veas el resultado antes de cerrar el navegador.
    time.sleep(5)
    print("Cerrando el navegador...")
    driver.quit()