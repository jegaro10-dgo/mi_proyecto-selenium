# app.py
from flask import Flask, render_template_string

# Inicializa la aplicación Flask
app = Flask(__name__)

# Define una página HTML simple en una variable
# Esta página es lo que tu prueba de Selenium 'verá'
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página de Prueba</title>
</head>
<body>
    <h1>¡Hola, esta es una página de prueba!</h1>
    <button id="miBoton">Haz clic aquí</button>
</body>
</html>
"""

# Crea una ruta para la página de inicio
@app.route('/')
def home():
    """
    Renderiza la página HTML cuando se accede a la ruta raíz.
    """
    return render_template_string(HTML_CONTENT)

# Inicia el servidor de desarrollo si el script se ejecuta directamente
if __name__ == '__main__':
    # La aplicación se ejecutará en el puerto 5000,
    # que es el mismo puerto que expone el Dockerfile
    app.run(host='0.0.0.0', port=5000)
