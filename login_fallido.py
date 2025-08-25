import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
def test_login_fallido():
    # 1. Inicializar el driver
    driver = webdriver.Chrome()

    try:
        # 2. Navegar a la página de login
        driver.get("https://demowebshop.tricentis.com/login")
        
        # 3. Encontrar los campos de email y contraseña
        email_input = driver.find_element(By.ID, "Email")
        password_input = driver.find_element(By.ID, "Password")

        # 4. Enviar los datos incorrectos
        email_input.send_keys("prueba@login.com")
        password_input.send_keys("test1234#")
        
        # 5. Encontrar y hacer clic en el botón de login
        login_button = driver.find_element(By.CLASS_NAME, "login-button")
        login_button.click()
        
        # 6. Esperar a que el mensaje de error aparezca
        wait = WebDriverWait(driver, 10)
        error_message = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'validation-summary-errors')]"))
        )
        
        # 7. Verificar que el mensaje sea el esperado
        expected_text = "Login was unsuccessful. Please correct the errors and try again."
        assert expected_text in error_message.text
        
        print(f"✅ ¡Prueba exitosa! El mensaje de error esperado '{expected_text}' se mostró correctamente.")

    finally:
        # 8. Cerrar el navegador al finalizar la prueba
        driver.quit()