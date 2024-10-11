from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
from pymongo import MongoClient, errors
import logging as log

app = FastAPI()

# Configuración de la conexión a MongoDB
try:
    client = MongoClient("mongodb://54.204.121.252:27013")  # IP y puerto correctos
    database_name = "sistema_biblioteca"
    editorial_collection = client[database_name]["Editorial"]
    editorial_data_collection = client[database_name]["Editorial_data"]
except errors.ConnectionFailure as e:
    log.error(f"Error de conexión: {e}")
    raise HTTPException(status_code=500, detail="No se pudo conectar a MongoDB")

# Configuración del logging
log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')

# Esquema para "Editorial"
class Editorial(BaseModel):
    ID: int
    nombre: str

# Esquema para "EditorialData" con los nuevos campos
class EditorialData(BaseModel):
    editorial_ID: int  # Referencia al ID de "Editorial"
    telefono: str  # Nuevo campo para teléfono
    direccion_oficina: str  # Nuevo campo para dirección de la oficina central
    RUC: str
    correo_electronico: EmailStr  # Validación de email
    pais_origen: str

# Clase para manejar las operaciones con MongoDB
class MongoAPI:
    def __init__(self, database: str, collection: str):
        try:
            self.client = MongoClient("mongodb://54.204.121.252:27013")
            self.collection = self.client[database][collection]
        except errors.ConnectionFailure as e:
            log.error(f"Error al conectar con MongoDB: {e}")
            raise HTTPException(status_code=500, detail="Error de conexión con la base de datos")

    def leer(self):
        try:
            log.info('Leyendo todos los datos')
            documentos = self.collection.find()
            return [{item: data[item] for item in data if item != '_id'} for data in documentos]
        except Exception as e:
            log.error(f"Error al leer datos: {e}")
            raise HTTPException(status_code=500, detail="Error al leer los datos")

    def escribir(self, documento: dict):
        try:
            log.info('Escribiendo datos')
            respuesta = self.collection.insert_one(documento)
            return {'Estado': 'Insertado exitosamente', 'ID_Documento': str(respuesta.inserted_id)}
        except Exception as e:
            log.error(f"Error al escribir datos: {e}")
            raise HTTPException(status_code=500, detail="Error al insertar el documento")

    def actualizar(self, filtro: dict, datos_actualizados: dict):
        try:
            log.info('Actualizando datos')
            respuesta = self.collection.update_one(filtro, {"$set": datos_actualizados})
            if respuesta.modified_count == 0:
                raise HTTPException(status_code=404, detail="Documento no encontrado para actualizar")
            return {'Estado': 'Actualizado exitosamente'}
        except Exception as e:
            log.error(f"Error al actualizar datos: {e}")
            raise HTTPException(status_code=500, detail="Error al actualizar los datos")

    def eliminar(self, filtro: dict):
        try:
            log.info('Eliminando datos')
            respuesta = self.collection.delete_one(filtro)
            if respuesta.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Documento no encontrado para eliminar")
            return {'Estado': 'Eliminado exitosamente'}
        except Exception as e:
            log.error(f"Error al eliminar datos: {e}")
            raise HTTPException(status_code=500, detail="Error al eliminar los datos")

# Rutas para la API de "Editorial"
@app.get("/editorial", response_model=List[Editorial])
def obtener_editorial():
    obj = MongoAPI(database_name, "Editorial")
    return obj.leer()

@app.post("/editorial", response_model=dict)
def crear_editorial(documento: Editorial):
    obj = MongoAPI(database_name, "Editorial")
    return obj.escribir(documento.dict())

@app.put("/editorial/{editorial_id}", response_model=dict)
def actualizar_editorial(editorial_id: int, datos_actualizados: Editorial):
    obj = MongoAPI(database_name, "Editorial")
    filtro = {"ID": editorial_id}
    return obj.actualizar(filtro, datos_actualizados.dict())

@app.delete("/editorial/{editorial_id}", response_model=dict)
def eliminar_editorial(editorial_id: int):
    obj = MongoAPI(database_name, "Editorial")
    filtro = {"ID": editorial_id}
    return obj.eliminar(filtro)

# Rutas para la API de "EditorialData"
@app.get("/editorial_data", response_model=List[EditorialData])
def obtener_editorial_data():
    obj = MongoAPI(database_name, "Editorial_data")
    return obj.leer()

@app.post("/editorial_data", response_model=dict)
def crear_editorial_data(documento: EditorialData):
    obj = MongoAPI(database_name, "Editorial_data")
    return obj.escribir(documento.dict())

@app.put("/editorial_data/{editorial_data_id}", response_model=dict)
def actualizar_editorial_data(editorial_data_id: int, datos_actualizados: EditorialData):
    obj = MongoAPI(database_name, "Editorial_data")
    filtro = {"editorial_ID": editorial_data_id}
    return obj.actualizar(filtro, datos_actualizados.dict())

@app.delete("/editorial_data/{editorial_data_id}", response_model=dict)
def eliminar_editorial_data(editorial_data_id: int):
    obj = MongoAPI(database_name, "Editorial_data")
    filtro = {"editorial_ID": editorial_data_id}
    return obj.eliminar(filtro)

# Ruta base para verificar el estado de la API
@app.get("/")
def base():
    return {"Estado": "Activo"}
