from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from pymongo import MongoClient
import logging as log

app = FastAPI()

# Configuración de la conexión a MongoDB
client = MongoClient("mongodb://54.204.121.252:27013")  # Cambia esto por la IP y puerto correctos
database_name = "sistema_biblioteca"  # Cambia esto por el nombre de tu base de datos
editorial_collection = client[database_name]["Editorial"]
editorial_data_collection = client[database_name]["Editorial_data"]

# Configuración del logging
log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')

# Esquema para "Editorial"
class Editorial(BaseModel):
    ID: int
    nombre: str

# Esquema para "EditorialData"
class EditorialData(BaseModel):
    editorial_ID: int  # Referencia al ID de "Editorial"
    fecha_registro: datetime
    RUC: str
    correo_electronico: str
    pais_origen: str

# Clase para manejar las operaciones con MongoDB
class MongoAPI:
    def __init__(self, database: str, collection: str):
        self.client = MongoClient("mongodb://54.204.121.252:27013")  # IP de la base de datos MongoDB
        self.collection = self.client[database][collection]

    def leer(self):
        log.info('Leyendo todos los datos')
        documentos = self.collection.find()
        return [{item: data[item] for item in data if item != '_id'} for data in documentos]

    def escribir(self, documento: dict):
        log.info('Escribiendo datos')
        respuesta = self.collection.insert_one(documento)
        return {'Estado': 'Insertado exitosamente', 'ID_Documento': str(respuesta.inserted_id)}

    def actualizar(self, filtro: dict, datos_actualizados: dict):
        log.info('Actualizando datos')
        respuesta = self.collection.update_one(filtro, {"$set": datos_actualizados})
        return {'Estado': 'Actualizado exitosamente' if respuesta.modified_count > 0 else "No se actualizó nada."}

    def eliminar(self, filtro: dict):
        log.info('Eliminando datos')
        respuesta = self.collection.delete_one(filtro)
        return {'Estado': 'Eliminado exitosamente' if respuesta.deleted_count > 0 else "Documento no encontrado."}

# Rutas para la API de "Editorial"
@app.get("/editorial", response_model=List[Editorial])
def obtener_editorial():
    obj = MongoAPI(database_name, "Editorial")
    respuesta = obj.leer()
    return respuesta

@app.post("/editorial", response_model=dict)
def crear_editorial(documento: Editorial):
    obj = MongoAPI(database_name, "Editorial")
    respuesta = obj.escribir(documento.dict())
    return respuesta

@app.put("/editorial/{editorial_id}", response_model=dict)
def actualizar_editorial(editorial_id: int, datos_actualizados: Editorial):
    obj = MongoAPI(database_name, "Editorial")
    filtro = {"ID": editorial_id}
    respuesta = obj.actualizar(filtro, datos_actualizados.dict())
    return respuesta

@app.delete("/editorial/{editorial_id}", response_model=dict)
def eliminar_editorial(editorial_id: int):
    obj = MongoAPI(database_name, "Editorial")
    filtro = {"ID": editorial_id}
    respuesta = obj.eliminar(filtro)
    return respuesta

# Rutas para la API de "EditorialData"
@app.get("/editorial_data", response_model=List[EditorialData])
def obtener_editorial_data():
    obj = MongoAPI(database_name, "Editorial_data")
    respuesta = obj.leer()
    return respuesta

@app.post("/editorial_data", response_model=dict)
def crear_editorial_data(documento: EditorialData):
    obj = MongoAPI(database_name, "Editorial_data")
    respuesta = obj.escribir(documento.dict())
    return respuesta

@app.put("/editorial_data/{editorial_data_id}", response_model=dict)
def actualizar_editorial_data(editorial_data_id: int, datos_actualizados: EditorialData):
    obj = MongoAPI(database_name, "Editorial_data")
    filtro = {"editorial_ID": editorial_data_id}
    respuesta = obj.actualizar(filtro, datos_actualizados.dict())
    return respuesta

@app.delete("/editorial_data/{editorial_data_id}", response_model=dict)
def eliminar_editorial_data(editorial_data_id: int):
    obj = MongoAPI(database_name, "Editorial_data")
    filtro = {"editorial_ID": editorial_data_id}
    respuesta = obj.eliminar(filtro)
    return respuesta

# Ruta base para verificar el estado de la API
@app.get("/")
def base():
    return {"Estado": "Activo"}
