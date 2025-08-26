import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

# --- Parte 1: Carga de datos de prueba ---
def get_users(filename="user_data.txt"):
    """
    Carga todos los datos de los usuarios desde el archivo y los retorna en una lista de diccionarios.
    """
    users = []
    current_user_data = {}
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line == "--- Nuevo Registro ---":
                    current_user_data = {}
                elif line.startswith("Email:"):
                    current_user_data['email'] = line.split(": ")[1]
                elif line.startswith("Password:"):
                    current_user_data['password'] = line.split(": ")[1]
                elif line == "----------------------":
                    if 'email' in current_user_data and 'password' in current_user_data:
                        users.append(current_user_data)
        return users
    except FileNotFoundError:
        pytest.skip(f"El archivo '{filename}' no se encontró. No se puede ejecutar la prueba.")
        return []

# --- Parte 2: El caso de prueba de pytest ---
@pytest.mark.parametrize("user_data", get_users())
def test_login_with_screenshot_on_fail(driver, user_data):
    """
    Prueba que el inicio de sesión sea exitoso para cada usuario en la lista.
    """
    EMAIL = user_data['email']
    PASSWORD = user_data['password']

    # Configurar el WebDriver para Chrome
    driver = webdriver.Chrome()

    try:
        # Navegar a la página de inicio de sesión
        print(f"Probando el inicio de sesión para el usuario: {EMAIL}")
        driver.get("https://demowebshop.tricentis.com/login")

        # Rellenar los campos del formulario de inicio de sesión
        wait = WebDriverWait(driver, 10)
        
        email_field = wait.until(EC.presence_of_element_located((By.ID, "Email")))
        email_field.send_keys(EMAIL)
        
        password_field = wait.until(EC.presence_of_element_located((By.ID, "Password")))
        password_field.send_keys(PASSWORD)
        
        # Hacer clic en el botón de inicio de sesión
        driver.find_element(By.CLASS_NAME, "login-button").click()

        # Verificar que el inicio de sesión fue exitoso
        wait.until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{EMAIL}')]")))
        print(f"¡Inicio de sesión exitoso para el usuario: {EMAIL}!")

    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_filename = f"screenshot_failure_{timestamp}.png"
        driver.save_screenshot(screenshot_filename)
        pytest.fail(f"La prueba de inicio de sesión falló para el usuario {EMAIL}. Se guardó una captura de pantalla: {screenshot_filename}. Causa: {e}")
    
    finally:
        pass