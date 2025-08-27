import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def pytest_addoption(parser):
    """
    Agrega la opción de línea de comandos --browser a pytest.
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Navegador para ejecutar las pruebas (chrome o firefox)",
    )

@pytest.fixture(scope="session")
def browser(request):
    """
    Fixture para pasar el nombre del navegador a la prueba.
    """
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def driver(browser):
    """
    Fixture que inicializa el WebDriver de Selenium basado en el navegador seleccionado.
    """
    if browser == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
    elif browser == "firefox":
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(options=firefox_options)
    else:
        raise ValueError(f"Navegador no soportado: {browser}")

    yield driver
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