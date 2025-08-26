import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from selenium.webdriver.chrome.options import Options

# Función para leer datos del archivo CSV
def leer_datos_productos():
    """Lee los datos de los productos desde un archivo CSV."""
    productos = []
    try:
        with open('data/productos_data.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader) # Omitir la fila de encabezados
            for row in reader:
                productos.append(row)
    except FileNotFoundError:
        pytest.fail("El archivo 'data/productos_data.csv' no fue encontrado.")
    return productos

# El fixture parametrizado ahora lee los datos del CSV y ejecuta una prueba por cada fila
@pytest.mark.parametrize("nombre_producto,precio,cantidad,sku,disponibilidad,color,categoria", leer_datos_productos())
def test_probar_productos(driver, nombre_producto, precio, cantidad, sku, disponibilidad, color, categoria):
    """
    Prueba la funcionalidad de búsqueda de productos utilizando datos de un CSV.
    Cada fila del CSV se convierte en una prueba independiente.
    """
    try:
        print(f"Buscando el producto: {nombre_producto} (Disponibilidad: {disponibilidad})")
        
        # Navegar a la página principal
        driver.get("https://demowebshop.tricentis.com/")

        # Encontrar el campo de búsqueda y escribir el nombre del producto
        search_box = driver.find_element(By.ID, "small-searchterms")
        search_box.send_keys(nombre_producto)
        
        # Presionar Enter para realizar la búsqueda
        search_box.send_keys(Keys.ENTER)
        
        # Buscar los enlaces de productos en los resultados de la búsqueda
        product_links = driver.find_elements(By.CLASS_NAME, "product-title")
        
        # Lógica de verificación basada en la disponibilidad del CSV
        if disponibilidad.lower() == 'si':
            # Si esperamos que esté, el número de enlaces de productos debe ser mayor que 0
            assert len(product_links) > 0, f"❌ Error: El producto '{nombre_producto}' no fue encontrado como se esperaba."
            print(f"✅ ¡Prueba exitosa! El producto '{nombre_producto}' fue encontrado.")
        else:
            # Si esperamos que no esté, el número de enlaces debe ser 0
            assert len(product_links) == 0, f"❌ Error: El producto '{nombre_producto}' fue encontrado, pero se esperaba que no lo estuviera."
            print(f"✅ ¡Prueba exitosa! El producto '{nombre_producto}' no fue encontrado como se esperaba.")

    except Exception as e:
        pytest.fail(f"La prueba para el producto '{nombre_producto}' falló. Causa: {e}")
