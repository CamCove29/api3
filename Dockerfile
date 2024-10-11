# Usa una imagen base de Python
FROM python:3-slim

# Establece el directorio de trabajo
WORKDIR /programas/api-editorial

# Instala las dependencias necesarias
RUN pip3 install flask
RUN pip3 install pymongo
RUN pip3 install flasgger  # Agrega Flasgger aquí

# Copia el contenido de la aplicación al contenedor
COPY . .

# Comando para ejecutar la aplicación
CMD [ "python3", "./app.py" ]
