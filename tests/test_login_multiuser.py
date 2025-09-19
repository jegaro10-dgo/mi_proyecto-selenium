from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import chromedriver_autoinstaller
import pytest

# --- Paso 1: Leer los datos del usuario desde el archivo ---
def load_users_from_file(filename="user_data.txt"):
    """
    Carga todos los datos de los usuarios desde el archivo y los retorna en una lista de diccionarios.
    """
    users = []
    current_user_data = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("Email:"):
                    if 'email' in current_user_data: # Guarda el usuario anterior si existe
                        users.append(current_user_data)
                    current_user_data = {'email': line.split(": ")[1]}
                elif line.startswith("Password:"):
                    current_user_data['password'] = line.split(": ")[1]
            
            if 'email' in current_user_data: # Guarda el último usuario
                users.append(current_user_data)
        return users
    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no se encontró.")
        return []

# Cargar todos los usuarios del archivo
users = load_users_from_file()

if not users:
    print("No se encontraron usuarios en el archivo para iniciar sesión.")
    exit()

# 2. Iniciar el navegador y envolver toda la prueba en un bloque try...finally
try:
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()

    # --- Bucle para iterar sobre cada usuario ---
    for test_user in users:
        EMAIL = test_user['email']
        PASSWORD = test_user['password']

        try:
            print(f"--- Iniciando prueba para el usuario: {EMAIL} ---")
            
            # Navegar a la página de inicio de sesión
            driver.get("https://demowebshop.tricentis.com/login")
            
            # Rellenar los campos del formulario de inicio de sesión
            wait = WebDriverWait(driver, 10)
            
            email_field = wait.until(EC.presence_of_element_located((By.ID, "Email")))
            password_field = wait.until(EC.presence_of_element_located((By.ID, "Password")))
            
            # Limpiar los campos antes de enviar nuevas credenciales
            email_field.clear()
            password_field.clear()
            
            email_field.send_keys(EMAIL)
            password_field.send_keys(PASSWORD)
            
            # Hacer clic en el botón de inicio de sesión
            driver.find_element(By.CLASS_NAME, "login-button").click()

            # Verificar que el inicio de sesión fue exitoso
            wait.until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{EMAIL}')]")))
            print(f"¡Inicio de sesión exitoso para {EMAIL}!")
            
            # Opcional: Cerrar sesión para el siguiente test
            driver.find_element(By.CLASS_NAME, "ico-logout").click()
            time.sleep(2)

        except Exception as e:
            print(f"Ocurrió un error con el usuario {EMAIL}: {e}")
            
finally:
    # Este bloque solo se ejecuta al final de todas las pruebas
    print("Todas las pruebas de inicio de sesión han terminado.")
    time.sleep(5)
    driver.quit()