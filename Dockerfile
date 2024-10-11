FROM python:3-slim
WORKDIR /programas/api-editorial
RUN pip3 install flask
RUN pip3 install pymongo
RUN pip3 install flasgger
RUN pip3 install pydantic
RUN pip3 install "fastapi[standard]"
RUN pip3 install pydantic

# Expone el puerto 8000
EXPOSE 8083

# Comando para ejecutar la aplicación FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8083"]
