from selenium import webdriver
from selenium.webdriver.common.by import By 
import time

driver = webdriver.Safari()

# Navega a una página web
driver.get("https://www.google.com")
# Espera unos segundos para ver la página 
time.sleep(5)
# Encuentra un elemento por su nombre (en este caso, el cuadro de búsqueda de Google) 
search_box = driver.find_element(By.NAME, "q")

# Escribe algo en el cuadro de búsqueda 
search_box.send_keys("Hola mundo")

# Espera otros segundos para ver los resultados 
time.sleep(5)
 # Cierra el navegador 
driver.quit()

print("Prueba automatizada completada con éxito.")