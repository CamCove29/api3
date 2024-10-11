# Usa una imagen oficial de Python 3.9 como base
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor (si lo tienes)
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación al contenedor
COPY . .

# Expone el puerto 8000 para Uvicorn
EXPOSE 8083

# Comando para ejecutar Uvicorn con la aplicación FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8083"]
