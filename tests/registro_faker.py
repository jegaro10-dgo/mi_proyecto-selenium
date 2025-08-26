import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import time
import os # Importar la librería para manejar archivos

def test_user_registration_exitoso(driver):
    """
    Prueba el registro de un usuario nuevo con datos aleatorios y verifica el éxito.
    """
    # Inicializar la librería Faker
    fake = Faker()

    # Generar datos de usuario aleatorios
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    password = "ContrasenaSegura123!" # Para simplificar, la contraseña es fija

    try:
        # 2. Navegar a la página de registro
        print("Navegando a la página de registro...")
        driver.get("https://demowebshop.tricentis.com/register")

        # 3. Rellenar el formulario de registro con datos aleatorios
        print("Rellenando el formulario de registro con datos generados...")
        wait = WebDriverWait(driver, 10)
        
        # Rellenar el género
        driver.find_element(By.ID, "gender-male").click() # O gender-female

        # Rellenar nombre y apellido
        wait.until(EC.presence_of_element_located((By.ID, "FirstName"))).send_keys(first_name)
        wait.until(EC.presence_of_element_located((By.ID, "LastName"))).send_keys(last_name)

        # Rellenar correo electrónico y contraseña
        wait.until(EC.presence_of_element_located((By.ID, "Email"))).send_keys(email)
        wait.until(EC.presence_of_element_located((By.ID, "Password"))).send_keys(password)
        wait.until(EC.presence_of_element_located((By.ID, "ConfirmPassword"))).send_keys(password)
        
        # 4. Hacer clic en el botón de registro
        print("Haciendo clic en el botón de registro...")
        driver.find_element(By.ID, "register-button").click()

        # 5. Verificar que el registro fue exitoso
        print("Verificando que el registro fue exitoso...")
        wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "result"), "Your registration completed"))
        print("¡Registro de usuario exitoso!")
        print(f"Usuario registrado: {email}")

        # --- Nuevo paso: Guardar los datos del usuario ---
        print("Guardando los datos del usuario en user_data.txt...")
        with open("user_data.txt", "a") as file:
            file.write(f"Email: {email}\n")
            file.write(f"Password: {password}\n")
            file.write(f"First Name: {first_name}\n")
            file.write(f"Last Name: {last_name}\n")
            file.write("----------------------\n")

        print("Datos guardados con éxito.")

    except Exception as e:
        pytest.fail(f"Ocurrió un error en la prueba: {e}")

