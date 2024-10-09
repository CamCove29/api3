from flask import Flask, request, json, Response
from pymongo import MongoClient
import logging as log

app = Flask(__name__)

class MongoAPI:
    def __init__(self, nombre_coleccion):
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')
        self.client = MongoClient("mongodb://172.31.44.64:27017")  # IP privada de la base de datos
        self.database = self.client['localizacion_db']  # Nombre de la base de datos
        self.coleccion = self.database[nombre_coleccion]  # Seleccionar la colección

    def leer(self):
        log.info('Leyendo todos los datos')
        documentos = self.coleccion.find()
        salida = [{item: datos[item] for item in datos if item != '_id'} for datos in documentos]
        return salida

    def escribir(self, datos):
        log.info('Escribiendo datos')
        nuevo_documento = datos['Documento']
        respuesta = self.coleccion.insert_one(nuevo_documento)
        salida = {'Estado': 'Insertado con éxito', 'ID_Documento': str(respuesta.inserted_id)}
        return salida

    def actualizar(self, datos):
        log.info('Actualizando datos')
        filtro = datos['Filtro']
        datos_actualizados = {"$set": datos['DatosAActualizar']}
        respuesta = self.coleccion.update_one(filtro, datos_actualizados)
        salida = {'Estado': 'Actualizado con éxito' if respuesta.modified_count > 0 else "Nada fue actualizado."}
        return salida

    def eliminar(self, datos):
        log.info('Eliminando datos')
        filtro = datos['Filtro']
        respuesta = self.coleccion.delete_one(filtro)
        salida = {'Estado': 'Eliminado con éxito' if respuesta.deleted_count > 0 else "Documento no encontrado."}
        return salida

@app.route('/')
def base():
    return Response(response=json.dumps({"Estado": "UP"}), status=200, mimetype='application/json')

@app.route('/ubicaciones', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gestionar_ubicaciones():
    datos = request.json
    accion = request.method

    api = MongoAPI('ubicacion')  # Seleccionar la colección de ubicaciones

    if accion == 'GET':
        respuesta = api.leer()
        return Response(response=json.dumps(respuesta), status=200, mimetype='application/json')

    if accion == 'POST':
        if not datos or 'Documento' not in datos:
            return Response(response=json.dumps({"Error": "Por favor proporciona la información de conexión"}), status=400, mimetype='application/json')
        respuesta = api.escribir(datos)
        return Response(response=json.dumps(respuesta), status=200, mimetype='application/json')

    if accion == 'PUT':
        if not datos or 'Filtro' not in datos:
            return Response(response=json.dumps({"Error": "Por favor proporciona la información de conexión"}), status=400, mimetype='application/json')
        respuesta = api.actualizar(datos)
        return Response(response=json.dumps(respuesta), status=200, mimetype='application/json')

    if accion == 'DELETE':
        if not datos or 'Filtro' not in datos:
            return Response(response=json.dumps({"Error": "Por favor proporciona la información de conexión"}), status=400, mimetype='application/json')
        respuesta = api.eliminar(datos)
        return Response(response=json.dumps(respuesta), status=200, mimetype='application/json')

@app.route('/historial', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gestionar_historial():
    datos = request.json
    accion = request.method

    api = MongoAPI('historial_localizacion')  # Seleccionar la colección de historial de localización

    if accion == 'GET':
        respuesta = api.leer()
        return Response(response=json.dumps(respuesta), status=200, mimetype='application/json')

    if accion == 'POST':
        if not datos or 'Documento' not in datos:
            return Response(response=json.dumps({"Error": "Por favor proporciona la información de conexión"}), status=400, mimetype='application/json')
        respuesta = api.escribir(datos)
        return Response(response=json.dumps(respuesta), status=200, mimetype='application/json')

    if accion == 'PUT':
        if not datos or 'Filtro' not in datos:
            return Response(response=json.dumps({"Error": "Por favor proporciona la información de conexión"}), status=400, mimetype='application/json')
        respuesta = api.actualizar(datos)
        return Response(response=json.dumps(respuesta), status=200, mimetype='application/json')

    if accion == 'DELETE':
        if not datos or 'Filtro' not in datos:
            return Response(response=json.dumps({"Error": "Por favor proporciona la información de conexión"}), status=400, mimetype='application/json')
        respuesta = api.eliminar(datos)
        return Response(response=json.dumps(respuesta), status=200, mimetype='application/json')

@app.route('/clientes/<cliente_id>/ubicacion', methods=['GET'])
def obtener_ubicacion_cliente(cliente_id):
    log.info(f'Obteniendo ubicación para el cliente {cliente_id}')
    api = MongoAPI('ubicacion')
    # Aquí puedes definir la lógica para obtener la ubicación del cliente
    ubicacion = api.coleccion.find_one({"cliente_id": int(cliente_id)})
    if ubicacion:
        return Response(response=json.dumps(ubicacion), status=200, mimetype='application/json')
    return Response(response=json.dumps({"Error": "Ubicación no encontrada"}), status=404, mimetype='application/json')

@app.route('/libros/<libro_id>/historial', methods=['GET'])
def obtener_historial_libro(libro_id):
    log.info(f'Obteniendo historial de ubicación para el libro {libro_id}')
    api = MongoAPI('historial_localizacion')
    # Aquí puedes definir la lógica para obtener el historial de localización del libro
    historial = api.coleccion.find({"libro_id": int(libro_id)})
    salida = list(historial)
    if salida:
        return Response(response=json.dumps(salida), status=200, mimetype='application/json')
    return Response(response=json.dumps({"Error": "Historial de ubicación no encontrado"}), status=404, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=False)
