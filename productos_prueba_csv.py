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

                # 4. Verificar que la búsqueda fue exitosa
                # VERIFICACIÓN: Lógica basada en tu idea
                if disponibilidad.lower() == 'si':
                    # Si esperamos que esté, el mensaje de "No products" NO debe aparecer.
                    try:
                        wait = WebDriverWait(driver, 5)
                        wait.until(
                            EC.presence_of_element_located((By.XPATH, "//strong[text()='No products were found that matched your criteria.']"))
                        )
                        # Si el mensaje apareció, la prueba falló.
                        assert False, f"❌ Error: El producto '{nombre_producto}' no fue encontrado como se esperaba."
                    except:
                        # Si el mensaje NO apareció (lo que esperamos), la prueba es exitosa.
                        print(f"✅ ¡Prueba exitosa! El producto '{nombre_producto}' fue encontrado.")
                
                else:
                    # Si esperamos que no esté, el mensaje de "No products" SÍ debe aparecer.
                    try:
                        wait = WebDriverWait(driver, 5)
                        wait.until(
                            EC.presence_of_element_located((By.XPATH, "//strong[text()='No products were found that matched your criteria.']"))
                        )
                        print(f"✅ ¡Prueba exitosa! El producto '{nombre_producto}' no fue encontrado como se esperaba.")
                    except:
                        # Si el mensaje NO apareció, la prueba falló.
                        assert False, f"❌ Error: El producto '{nombre_producto}' fue encontrado, pero se esperaba que no lo estuviera."

                time.sleep(3)
    finally:
        # 5. Cerrar el navegador al final de la prueba
        # (Esto también debe ir dentro del bucle para que se cierre después de cada prueba)
        driver.quit()