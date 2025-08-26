import pytest
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="function")
def driver():
    """
    Este fixture configura el driver de Selenium.
    Se ejecuta una vez por cada prueba ('function').
    """
    # Configuración de las opciones del navegador
    chrome_options = Options()
    # Ejecutar en modo sin cabeza (headless), lo cual es necesario en entornos de CI como GitHub Actions.
    chrome_options.add_argument("--headless")
    # Argumentos adicionales para una ejecución más robusta en entornos de servidor.
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Iniciar el driver
    # Selenium ahora gestionará la instalación del driver automáticamente.
    driver = webdriver.Chrome(options=chrome_options)
    
    # 'yield' devuelve el control a la prueba que lo llamó.
    yield driver
    
    # Después de que la prueba se ejecuta, este código limpia y cierra el navegador.
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Esto es un 'hook' que Pytest ejecuta para cada paso de la prueba
    # Usamos hookwrapper para tener acceso al resultado
    outcome = yield
    report = outcome.get_result()

    # Si la prueba falló y es una prueba de 'call' (el cuerpo principal)
    if report.when == "call" and report.failed:
        # Aseguramos que el fixture 'driver' esté disponible
        try:
            driver = item.funcargs.get('driver')
            if driver:
                # Tomamos la captura de pantalla
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                screenshot_filename = f"failure_{item.name}_{timestamp}.png"
                driver.save_screenshot(screenshot_filename)
                print(f"\n¡Prueba fallida! Se guardó una captura de pantalla: {screenshot_filename}")
        except Exception as e:
            print(f"Error al tomar la captura de pantalla: {e}")