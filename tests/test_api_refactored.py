# Archivo: tests/test_api_refactored.py
import requests
import pytest

# Lista de URLs de endpoints de prueba para verificar
API_URLS = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3",
    "https://jsonplaceholder.typicode.com/todos/1"
]

@pytest.mark.parametrize("url", API_URLS)
def test_get_api_endpoint(url):
    """
    Prueba que un endpoint de la API responde correctamente.
    Esta prueba se ejecutará para cada URL en la lista API_URLS.
    """
    try:
        # Hacer una solicitud HTTP GET al endpoint
        print(f"Probando la URL: {url}")
        response = requests.get(url, timeout=10) # Añadir un timeout para evitar que se quede "colgado"
        
        # Afirmar que el código de estado de la respuesta es 200 (OK)
        assert response.status_code == 200, f"Error: Se esperaba el código de estado 200 para {url}, pero se obtuvo {response.status_code}"
        
        # Afirmar que el contenido de la respuesta tiene el formato JSON
        data = response.json()
        assert isinstance(data, dict), f"Error: El contenido de la respuesta para {url} no es un diccionario JSON válido"
        
        # Afirmar que la respuesta contiene las claves esperadas
        expected_keys = ["id", "userId"]
        missing_keys = [key for key in expected_keys if key not in data]
        assert not missing_keys, f"Error: Faltan las siguientes claves en la respuesta para {url}: {', '.join(missing_keys)}"
            
        print(f"La prueba de API para {url} pasó exitosamente!")
    
    except requests.exceptions.RequestException as e:
        pytest.fail(f"La prueba para {url} falló debido a un error de conexión: {e}")
