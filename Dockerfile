# Usa una imagen base de Python.
FROM python:3.9-slim

# Establece el directorio de trabajo en /app.
WORKDIR /app

# Copia los archivos de requerimientos y del proyecto al contenedor.
COPY requirements.txt .
COPY . .

# Instala las dependencias del proyecto.
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que la aplicación escuchará.
EXPOSE 5000

# Define el comando para ejecutar la aplicación cuando el contenedor inicie.
CMD ["python", "app.py"]
