import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import time

# Datos de la cuenta de prueba
USUARIO = "prueba_selenium"
LASTNAME = "pruebaTres"
EMAIL = "prueba_selenium@example.com"
CONTRASENA = "ContrasenaSegura123!"

def test_registro_email_vacio(driver):
    """
    Prueba que el registro falle si se deja el campo de email vacío.
    """
    try:
        # 2. Navegar a la página de registro
        print("Abriendo la página de registro...")
        driver.get("https://demowebshop.tricentis.com/register")
        
        # 3. Rellenar los campos del formulario, pero dejando el email vacío
        print("Rellenando el formulario de registro, dejando el campo de email vacío")

        # Esperar a que los campos del formulario estén visibles
        wait = WebDriverWait(driver, 10)
        
        # Rellenar el campo 'gender' (género) - seleccionamos "Male"
        driver.find_element(By.ID, "gender-male").click()
        
        # Rellenar el campo 'first name' (nombre)
        driver.find_element(By.ID, "FirstName").send_keys(USUARIO)
        
        # Rellenar el campo 'last name' (apellido)
        driver.find_element(By.ID, "LastName").send_keys(LASTNAME)
        
        # Rellenar el campo 'email'
        # Lo omitimos para la prueba
        
        # Rellenar el campo 'password'
        driver.find_element(By.ID, "Password").send_keys(CONTRASENA)
        
        # Rellenar el campo 'confirm password'
        driver.find_element(By.ID, "ConfirmPassword").send_keys(CONTRASENA)
        
        # 4. Hacer clic en el botón de registro
        print("Haciendo clic en el botón de registro...")
        driver.find_element(By.ID, "register-button").click()

        # 5. Verificar que se muestre el mensaje de error del campo de email
        print("Verificando el mensaje de error del campo de email...")
        expected_error_text = "Email is required."
        
        # Espera hasta que el mensaje de error del email sea visible
        # El mensaje de error para el email tiene la clase 'field-validation-error'
        # y contiene el texto 'Email is required.'.
        error_message_element = wait.until(
         EC.presence_of_element_located((By.XPATH, f"//span[text()='{expected_error_text}']"))
        )

        # Afirmar que el texto del mensaje es el esperado
        print(f"¡Prueba exitosa! se encontró el mensaje de error: '{expected_error_text}'.")

    except Exception as e:
        pytest.fail(f"Ocurrió un error en la prueba: {e}")
