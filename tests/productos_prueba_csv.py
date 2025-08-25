from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from selenium import webdriver
# Puedes agregar aquí otros imports que necesites, como By, WebDriverWait, etc.

def test_probar_productos():
    # Inicializar el driver (esto va ANTES del bucle for)
    driver = webdriver.Chrome()
    try: 
        # Código para leer el archivo CSV
        with open('data/productos_data.csv', 'r') as file:
            reader = csv.reader(file)
            # La primera fila son los encabezados, la omitimos
            next(reader) 
    
            for row in reader:
                # Extraemos los datos de la fila
                nombre_producto = row[0]
                precio = row[1]
                cantidad = row[2]
                sku = row[3]
                disponibilidad = row[4]
                color = row[5]
                categoria = row[6]

                print(f"Buscando el producto: {nombre_producto} (Disponibilidad: {disponibilidad})")
                driver.get("https://demowebshop.tricentis.com/")

                # 1. Navegar a la página principal
                print(f"Buscando el producto: {nombre_producto}")
                driver.get("https://demowebshop.tricentis.com/")

                # 2. Encontrar el campo de búsqueda y escribir el nombre del producto
                search_box = driver.find_element(By.ID, "small-searchterms")
                search_box.send_keys(nombre_producto)
                
                # 3. Presionar Enter para realizar la búsqueda
                search_box.send_keys(Keys.ENTER)
                # Aquí es donde buscamos los enlaces de productos.
                # Nota la 's' al final de find_elements
                product_links = driver.find_elements(By.CLASS_NAME, "product-title")
                
                # 4. Verificar que la búsqueda fue exitosa
                # VERIFICACIÓN: Lógica basada en tu idea
                if disponibilidad.lower() == 'si':
                # Si esperamos que esté, el número de enlaces de productos debe ser mayor que 0
                    assert len(product_links) > 0, f"❌ Error: El producto '{nombre_producto}' no fue encontrado como se esperaba."
                    print(f"✅ ¡Prueba exitosa! El producto '{nombre_producto}' fue encontrado.")
                else:
                # Si esperamos que no esté, el número de enlaces debe ser 0
                    assert len(product_links) == 0, f"❌ Error: El producto '{nombre_producto}' fue encontrado, pero se esperaba que no lo estuviera."
                    print(f"✅ ¡Prueba exitosa! El producto '{nombre_producto}' no fue encontrado como se esperaba.")

            time.sleep(2)
    finally:
        # 5. Cerrar el navegador al final de la prueba
        # (Esto también debe ir dentro del bucle para que se cierre después de cada prueba)
        driver.quit()