from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
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
    
    # 6. Buscar el producto "Computing and Internet"
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
    print("¡Producto añadido, iniciando el proceso de checkout!...")

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
  

except Exception as e:
    print(f"Ocurrió un error en la prueba: {e}")

finally:
    # Pausar 5 segundos para que veas el resultado antes de cerrar el navegador.
    time.sleep(5)
    print("Cerrando el navegador...")
    driver.quit()