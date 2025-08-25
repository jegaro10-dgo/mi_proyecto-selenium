from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Datos de la cuenta de prueba
EMAIL = "jegaro10@gmail.com"
CONTRASENA = "SY6-GS@+rT6Mj$b"

# 1. Configurar el WebDriver para Chrome
driver = webdriver.Chrome()

try:
    # 2. Navegar a la página de inicio de sesión
    print("Abriendo la página de inicio de sesión")
    driver.get("https://bebbia.com/login/")
    
    # 3. Rellenar los campos del formulario de inicio de sesión
    print("Rellenando el campo de correo electrónico")

    # Esperar a que los campos del formulario estén visibles
    wait = WebDriverWait(driver, 10)
    
    # Rellenar el campo 'email'
    email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    email_field.send_keys(EMAIL)

    # 4. Hacer clic en el botón siguiente
    print("Hacer click en el botón siguiente...")
    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Siguiente']")))
    next_button.click()

    # 5. Rellenar el campo 'password'
    print("Rellenando el campo de contraseña...")
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_field.send_keys(CONTRASENA)
    
    # 6. Hacer clic en el botón de inicio de sesión
    print("Haciendo clic en el botón de inicio de sesión...")
    login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "button-primary")))
    login_button.click()

    # 7. Verificar que el inicio de sesión fue exitoso
    print("Verificando que el inicio de sesión fue exitoso...")
    # Para la verificación, podemos buscar un elemento que solo aparezca después de iniciar sesión,
    # como un enlace al dashboard o un elemento con el nombre del usuario.
    # Inspeccionando la página, un buen elemento podría ser el icono del carrito de compras.
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Mis suscripciones')]")))
    print("¡Inicio de sesión en Bebbia exitoso!")

except Exception as e:
    print(f"Ocurrió un error en la prueba: {e}")

finally:
    # Pausar 5 segundos para que veas el resultado antes de cerrar el navegador
    time.sleep(5)
    # 6. Cerrar el navegador
    print("Cerrando el navegador...")
    driver.quit()
