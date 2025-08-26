import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from selenium.webdriver.chrome.options import Options

# Datos de la cuenta de prueba
USUARIO = "prueba_selenium"
LASTNAME = "pruebaTres"
EMAIL = "prueba_selenium@example.com"
CONTRASENA = "ContrasenaSegura123!"

def test_login_fallido(driver):
    """
    Prueba que el registro falle cuando el email ya existe.
    """
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

        # 5. Verificar que el registro fallò con el mensaje de error espeado
        print("Verificando el mensaje de error...")
        
        # Espera hasta que el mensaje de error sea visible
        error_message_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'validation-summary-errors')]"))
        )

        # Afirmar que el texto del mensaje es el esperado
        expected_error_text = "The specified email already exists"
        assert expected_error_text in error_message_element.text
        print(f"¡Prueba exitosa! El mensaje de error '{expected_error_text}' fue encontrado.")

    except Exception as e:
        pytest.fail(f"Ocurrió un error en la prueba: {e}")
