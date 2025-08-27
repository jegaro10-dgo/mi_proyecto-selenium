# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de requerimientos e instálalos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación al directorio de trabajo
# ¡ESTA ES LA LÍNEA CLAVE QUE FALTA!
COPY . .

# Expone el puerto que la aplicación escuchará
EXPOSE 5000

# Define el comando para ejecutar la aplicación cuando el contenedor se inicie
CMD ["python", "app.py"]