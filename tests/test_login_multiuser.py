import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Fixture para inicializar y cerrar el navegador ---
@pytest.fixture(scope="module")
def driver():
    print("\nInicializando WebDriver en modo headless...")
    # Configurar las opciones de Chrome para el modo headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver_instance = webdriver.Chrome(options=options)
    yield driver_instance
    print("\nCerrando WebDriver...")
    driver_instance.quit()

# --- Funciones de soporte para leer los datos del usuario ---
def load_users_from_file(filename="user_data.txt"):
    users = []
    current_user_data = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("Email:"):
                    if 'email' in current_user_data:
                        users.append(current_user_data)
                    current_user_data = {'email': line.split(": ")[1]}
                elif line.startswith("Password:"):
                    current_user_data['password'] = line.split(": ")[1]
            
            if 'email' in current_user_data:
                users.append(current_user_data)
        return users
    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no se encontró.")
        return []

# --- Generar los parámetros de prueba a partir del archivo ---
@pytest.mark.parametrize("user", load_users_from_file())
def test_login(driver, user):
    """Prueba de login para cada usuario."""
    email = user['email']
    password = user['password']
    
    print(f"--- Iniciando prueba para el usuario: {email} ---")
    
    # Navegar a la página de inicio de sesión
    driver.get("https://demowebshop.tricentis.com/login")
    
    # Rellenar los campos
    wait = WebDriverWait(driver, 10)
    
    email_field = wait.until(EC.presence_of_element_located((By.ID, "Email")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "Password")))
    
    email_field.clear()
    password_field.clear()
    
    email_field.send_keys(email)
    password_field.send_keys(password)
    
    # Clic en el botón
    driver.find_element(By.CLASS_NAME, "login-button").click()

    # Verificar login exitoso
    wait.until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{email}')]")))
    print(f"¡Inicio de sesión exitoso para {email}!")
    
    # Cerrar sesión para la siguiente prueba
    driver.find_element(By.CLASS_NAME, "ico-logout").click()
    time.sleep(2)