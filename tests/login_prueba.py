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
    print("Abriendo la página de inicio de sesión")
    driver.get("https://demowebshop.tricentis.com/login")
    
    # 3. Rellenar los campos del formulario de inicio de sesión
    print("Rellenando el formulario de inicio de sesión")

    # Esperar a que los campos del formulario estén visibles
    wait = WebDriverWait(driver, 10)
    
    # Rellenar el campo 'email'
    email_field = wait.until(EC.presence_of_element_located((By.ID, "Email")))
    email_field.send_keys(EMAIL)
    
    # Rellenar el campo 'password'
    password_field = wait.until(EC.presence_of_element_located((By.ID, "Password")))
    password_field.send_keys(CONTRASENA)
    
    # 4. Hacer clic en el botón de inicio de sesión
    print("Haciendo clic en el botón de inicio de sesión...")
    driver.find_element(By.CLASS_NAME, "login-button").click()

    # 5. Verificar que el inicio de sesión fue exitoso
    print("Verificando que el inicio de sesión fue exitoso...")
    
    # Espera hasta que email del usuario aparezca en la cabecera
    logged_in_email = wait.until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{EMAIL}')]")))

    # Verificar que el texto del elemento es el email que usamos
    assert logged_in_email.text == EMAIL
    print(f"¡Prueba fue exitosa! El usuario '{EMAIL}' ha iniciado sesión correctamente.")

except Exception as e:
    print(f"Ocurrió un error en la prueba: {e}")

finally:
    # Pausar 5 segundos para que veas el resultado antes de cerrar el navegador
    time.sleep(5)
    # 6. Cerrar el navegador
    print("Cerrando el navegador...")
    driver.quit()
