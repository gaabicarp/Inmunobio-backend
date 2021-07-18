from servicios.productoService import ProductoService
from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request,jsonify
from exceptions.exception import ErrorProductoInexistente,ErrorDistribuidoraInexistente
from marshmallow import ValidationError

class ProductoResource(Resource):
    def post(self):
        datos = request.get_json()
        if(datos):
            try:
                return ProductoService().altaProducto(datos),200
                #aca devuelve el id del producto para luego pasarselo a l subida del archivo
                #y guardar el archivo con esa id
            except ValidationError as err:
                return {'Error': err.messages},400
            except ErrorDistribuidoraInexistente as err:
                return {'Error': err.message},400 
        return {'Error': 'Deben indicarse datos para el alta del producto'},400

    def put(self):
        datos = request.get_json()
        if(datos):
            try:
                ProductoService().modificarProducto(datos)
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'error': err.messages},400
            except ErrorProductoInexistente as err:
                return {'Error': err.message},400
        return {'Error': 'Deben indicarse datos para modificar el producto'},400

class ObtenerProductosResource(Resource):
    def get(self):
        return jsonify(ProductoService.obtenerProductos())
    
class ProductoID(Resource):
    def get(self,id_producto):
        if(id_producto):
            try:
                return ProductoService().obtenerProducto(id_producto)
            except ErrorProductoInexistente as err:
                return {'Error': err.message},400
        return {'Error': 'Debe indicarse id_producto'},400

    def delete(self,id_producto):
        #ver: borramos el producto ¿que sucede con los productos activos en stock? -> se preg primero
        #si llega aca quiere decir q ya se valido
        if(id_producto):
            try:
                ProductoService().bajaProducto(id_producto)
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'error': err.messages},400
            except ErrorProductoInexistente as err:
                return {'Error': err.message},400   
        return {'Error': 'Debe indicarse id_producto'},400

class ArchivoProducto(Resource):
    def post(self,id_producto):
        archivo = request.files['detallesTecnicos']
        if(archivo):
            try:
                ProductoService().asociarArchivo(archivo,id_producto)
                return {'Status':'ok'} ,200
            except ErrorProductoInexistente as err:
                return {'Error': err.message},400
            except:
                return {'Error':'no se pudo borrar archivo al hacer el update'},400
        return {'Error': 'Debe subirse el archivo correspondiente al campo detallesTecnicos'},400
