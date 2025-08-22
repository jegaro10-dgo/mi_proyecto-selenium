from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Datos de la cuenta de prueba
USUARIO = "prueba_selenium"
LASTNAME = "pruebaTres"
EMAIL = "prueba_selenium@example.com"
CONTRASENA = "ContrasenaSegura123!"

# 1. Configurar el WebDriver para Chrome
driver = webdriver.Chrome()

try:
    # 2. Navegar a la página de registro
    print("Abriendo la página de registro...")
    driver.get("https://demowebshop.tricentis.com/register")
    
    # 3. Rellenar los campos del formulario
    print("Rellenando el formulario de registro...")

    # Esperar a que los campos del formulario estén visibles
    wait = WebDriverWait(driver, 10)
    
    # Rellenar el campo 'gender' (género) - seleccionamos "Male"
    driver.find_element(By.ID, "gender-male").click()
    
    # Rellenar el campo 'first name' (nombre)
    driver.find_element(By.ID, "FirstName").send_keys(USUARIO)
    
    # Rellenar el campo 'last name' (apellido)
    driver.find_element(By.ID, "LastName").send_keys(LASTNAME)
    
    # Rellenar el campo 'email'
    driver.find_element(By.ID, "Email").send_keys(EMAIL)
    
    # Rellenar el campo 'password'
    driver.find_element(By.ID, "Password").send_keys(CONTRASENA)
    
    # Rellenar el campo 'confirm password'
    driver.find_element(By.ID, "ConfirmPassword").send_keys(CONTRASENA)
    
    # 4. Hacer clic en el botón de registro
    print("Haciendo clic en el botón de registro...")
    driver.find_element(By.ID, "register-button").click()

    # 5. Verificar que el registro fue exitoso
    print("Verificando el mensaje de éxito...")
    
    # Espera hasta que el mensaje de éxito sea visible
    success_message = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "result"))
    )

    # Afirmar que el texto del mensaje es el esperado
    assert success_message.text == "Your registration completed"
    print("¡Prueba exitosa! El mensaje 'Your registration completed' fue encontrado.")

except Exception as e:
    print(f"Ocurrió un error en la prueba: {e}")

finally:
    # Pausar 5 segundos para que veas el resultado antes de cerrar el navegador
    time.sleep(5)
    # 6. Cerrar el navegador
    print("Cerrando el navegador...")
    driver.quit()
