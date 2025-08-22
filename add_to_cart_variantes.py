from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Datos de la cuenta de prueba
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
    
    # 6. Buscar el producto "Build your own computer"
    print("Buscando el producto 'Build your own computer'...")
    search_box = wait.until(EC.presence_of_element_located((By.ID, "small-searchterms")))
    search_box.send_keys("Build your own computer")
    search_box.send_keys(Keys.RETURN)

    # 7. Hacer clic en el resultado de la búsqueda para ir a la página del producto
    print("Haciendo clic en el resultado de la búsqueda...")
    product_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Build your own computer")))
    product_link.click()

    # 8. Seleccionar las variantes de procesador y RAM
    print("Seleccionando variantes...")
    
    # Seleccionar el procesador "2.5 GHz Intel Pentium Dual-Core E2200 +15"
    processor_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='product_attribute_16_5_4']/option[@value='13']")))
    processor_option.click()
    
    # Seleccionar la RAM "8GB"
    ram_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='product_attribute_16_6_5']/option[@value='17']")))
    ram_option.click()

     # Seleccionar el HDD"
    hdd_option = wait.until(EC.element_to_be_clickable((By.ID, "product_attribute_16_3_6_19")))
    hdd_option.click()

    # Seleccionar el OS"
    os_option = wait.until(EC.element_to_be_clickable((By.ID, "product_attribute_16_4_7_21")))
    os_option.click()

    # Seleccionar el SW"
    # Manejando las opciones de software
    print("Seleccionando opciones de software...")
    
    # Localizador para el software por defecto (Microsoft office)
    microsoft_office_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "product_attribute_16_8_8_22")))

    # Si está seleccionado por defecto, lo deseleccionamos
    if microsoft_office_checkbox.is_selected():
        microsoft_office_checkbox.click()
    
    # Ahora seleccionamos el software que queremos, por ejemplo, Total commander
    total_commander_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "product_attribute_16_8_8_24")))
    microsoft_office_checkbox.click()
    
    # También puedes seleccionar más de una opción si lo deseas
    # total_commander_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "product_attribute_6_14")))
    # total_commander_checkbox.click()


    # 9. Añadir el producto al carrito
    print("Añadiendo el producto al carrito...")
    add_to_cart_button = wait.until(EC.presence_of_element_located((By.ID, "add-to-cart-button-16")))
    add_to_cart_button.click()
    
    # 10. Verificar que el producto se añadió
    print("Verificando que el producto se añadió al carrito...")
    wait.until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "bar-notification.success"),
            "The product has been added to your shopping cart"
        )
    )
    
    print("¡Prueba exitosa! El mensaje de confirmación fue encontrado.")

except Exception as e:
    print(f"Ocurrió un error en la prueba: {e}")

finally:
    # Pausar 5 segundos para que veas el resultado antes de cerrar el navegador.
    time.sleep(5)
    print("Cerrando el navegador...")
    driver.quit()