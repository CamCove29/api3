from flask import Flask, request, json, Response
from pymongo import MongoClient
import logging as log

app = Flask(__name__)

# Clase para manejar las operaciones con MongoDB
class MongoAPI:
    def __init__(self, data):
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')
        self.client = MongoClient("mongodb://54.204.121.252:27013")  # IP de la base de datos MongoDB
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    # Método para leer los documentos de la colección
    def leer(self):
        log.info('Leyendo todos los datos')
        documentos = self.collection.find()
        salida = [{item: data[item] for item in data if item != '_id'} for data in documentos]
        return salida

    # Método para escribir un nuevo documento en la colección
    def escribir(self, data):
        log.info('Escribiendo datos')
        nuevo_documento = data['Documento']
        respuesta = self.collection.insert_one(nuevo_documento)
        salida = {'Estado': 'Insertado exitosamente',
                  'ID_Documento': str(respuesta.inserted_id)}
        return salida

    # Método para actualizar un documento en la colección
    def actualizar(self):
        log.info('Actualizando datos')
        filtro = self.data['Filtro']
        datos_actualizados = {"$set": self.data['DatosActualizados']}
        respuesta = self.collection.update_one(filtro, datos_actualizados)
        salida = {'Estado': 'Actualizado exitosamente' if respuesta.modified_count > 0 else "No se actualizó nada."}
        return salida

    # Método para eliminar un documento en la colección
    def eliminar(self, data):
        log.info('Eliminando datos')
        filtro = data['Filtro']
        respuesta = self.collection.delete_one(filtro)
        salida = {'Estado': 'Eliminado exitosamente' if respuesta.deleted_count > 0 else "Documento no encontrado."}
        return salida


# Ruta base para verificar el estado de la API
@app.route('/')
def base():
    return Response(response=json.dumps({"Estado": "Activo"}),
                    status=200,
                    mimetype='application/json')


# API para la tabla "Editorial"
@app.route('/editorial', methods=['GET'])
def obtener_editorial():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Por favor proporcione la información de conexión"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    respuesta = obj1.leer()
    return Response(response=json.dumps(respuesta),
                    status=200,
                    mimetype='application/json')

@app.route('/editorial', methods=['POST'])
def crear_editorial():
    data = request.json
    if data is None or data == {} or 'Documento' not in data:
        return Response(response=json.dumps({"Error": "Por favor proporcione la información de conexión"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    respuesta = obj1.escribir(data)
    return Response(response=json.dumps(respuesta),
                    status=200,
                    mimetype='application/json')

@app.route('/editorial', methods=['PUT'])
def actualizar_editorial():
    data = request.json
    if data is None or data == {} or 'Filtro' not in data:
        return Response(response=json.dumps({"Error": "Por favor proporcione la información de conexión"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    respuesta = obj1.actualizar()
    return Response(response=json.dumps(respuesta),
                    status=200,
                    mimetype='application/json')

@app.route('/editorial', methods=['DELETE'])
def eliminar_editorial():
    data = request.json
    if data is None or data == {} or 'Filtro' not in data:
        return Response(response=json.dumps({"Error": "Por favor proporcione la información de conexión"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    respuesta = obj1.eliminar(data)
    return Response(response=json.dumps(respuesta),
                    status=200,
                    mimetype='application/json')


# API para la tabla "Editorial_data"
@app.route('/editorial_data', methods=['GET'])
def obtener_editorial_data():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Por favor proporcione la información de conexión"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    respuesta = obj1.leer()
    return Response(response=json.dumps(respuesta),
                    status=200,
                    mimetype='application/json')

@app.route('/editorial_data', methods=['POST'])
def crear_editorial_data():
    data = request.json
    if data is None or data == {} or 'Documento' not in data:
        return Response(response=json.dumps({"Error": "Por favor proporcione la información de conexión"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    respuesta = obj1.escribir(data)
    return Response(response=json.dumps(respuesta),
                    status=200,
                    mimetype='application/json')

@app.route('/editorial_data', methods=['PUT'])
def actualizar_editorial_data():
    data = request.json
    if data is None or data == {} or 'Filtro' not in data:
        return Response(response=json.dumps({"Error": "Por favor proporcione la información de conexión"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    respuesta = obj1.actualizar()
    return Response(response=json.dumps(respuesta),
                    status=200,
                    mimetype='application/json')

@app.route('/editorial_data', methods=['DELETE'])
def eliminar_editorial_data():
    data = request.json
    if data is None or data == {} or 'Filtro' not in data:
        return Response(response=json.dumps({"Error": "Por favor proporcione la información de conexión"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    respuesta = obj1.eliminar(data)
    return Response(response=json.dumps(respuesta),
                    status=200,
                    mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085, debug=False)

