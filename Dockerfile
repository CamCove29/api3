# Usar una imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de la aplicación y el requirements.txt al contenedor
COPY app.py ./
COPY requirements.txt ./

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8001

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
