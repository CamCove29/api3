FROM python:3-slim
WORKDIR /programas/api-editorial
RUN pip install --no-cache-dir -r requirements.txt\
    && pip3 install pymongo \
    && pip3 install flasgger \
    && pip3 install pydantic \
    && pip3 install "fastapi[standard]" \
    && pip3 install pydantic

# Expone el puerto 8000
EXPOSE 8083

# Comando para ejecutar la aplicación FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8083"]
