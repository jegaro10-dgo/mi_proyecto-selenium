from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Paso 1: Leer los datos del usuario desde el archivo ---
def load_users_from_file(filename="user_data.txt"):
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
        print(f"Error: El archivo '{filename}' no se encontró.")
        return []

# Cargar todos los usuarios del archivo
users = load_users_from_file()

if not users:
    print("No se encontraron usuarios en el archivo para iniciar sesión. Por favor, ejecuta el script de registro primero.")
    exit()

# Seleccionar el usuario de la lista para la prueba

test_user = users[1]
EMAIL = test_user['email']
PASSWORD = test_user['password']

print(f"Datos leídos. Iniciando sesión con: {EMAIL}")

# 2. Configurar el WebDriver para Chrome
driver = webdriver.Chrome()

try:
    # 3. Navegar a la página de inicio de sesión
    print("Abriendo la página de inicio de sesión...")
    driver.get("https://demowebshop.tricentis.com/login")
    
    # 4. Rellenar los campos del formulario de inicio de sesión
    print("Rellenando el formulario de inicio de sesión...")
    wait = WebDriverWait(driver, 10)
    
    email_field = wait.until(EC.presence_of_element_located((By.ID, "Email")))
    email_field.send_keys(EMAIL)
    
    password_field = wait.until(EC.presence_of_element_located((By.ID, "Password")))
    password_field.send_keys(PASSWORD)
    
    # 5. Hacer clic en el botón de inicio de sesión
    print("Haciendo clic en el botón de inicio de sesión...")
    driver.find_element(By.CLASS_NAME, "login-button").click()

    # 6. Verificar que el inicio de sesión fue exitoso
    print("Verificando que el inicio de sesión fue exitoso...")
    wait.until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{EMAIL}')]")))
    print("¡Inicio de sesión exitoso!")
    
except Exception as e:
    print(f"Ocurrió un error en la prueba: {e}")

finally:
    # Pausar para que puedas ver el resultado.
    time.sleep(5)
    print("Cerrando el navegador...")
    driver.quit()