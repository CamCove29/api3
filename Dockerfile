# Usa una imagen base de Python
FROM python:3-slim

# Establece el directorio de trabajo
WORKDIR /programas/api-editorial

# Instala las dependencias necesarias
RUN pip3 install flask pymongo flasgger gunicorn  # Agrega Gunicorn aquí

# Copia el contenido de la aplicación al contenedor
COPY . .

# Comando para ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8083", "app:app"]
