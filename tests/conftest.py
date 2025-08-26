import pytest
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver(request):
    """Crea una instancia de WebDriver y la cierra al finalizar la prueba."""
    print("\nIniciando el navegador...")
    
    # Configuración para ejecutar en modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    driver.set_window_size(1929, 1080)
    yield driver  # Esto es lo que se retorna a la prueba
    
    # Esta parte se ejecuta después de que la prueba termina
    print("\nCerrando el navegador...")
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