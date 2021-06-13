from servicios.productoService import ProductoService
from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request

class ProductoResource(Resource):
    def post(self):
        datos = request.get_json()
        if(datos):
            return ProductoService().altaProducto(datos)
        return {'name': 'None'},400

    def put(self):
        datos = request.get_json()
        if(datos):
            return ProductoService().modificarProducto(datos)
        return {'name': 'None'},400
    
class ObtenerProductosResource(Resource):
    def get(self):
        return ProductoService().obtenerProductos()
    
class ProductoID(Resource):
    def get(self,id_producto):
        return ProductoService().obtenerProducto(id_producto)

    def delete(self,id_producto):
        #ver: borramos el producto ¿que sucede con los productos activos en stock? -> se preg primero
        #si llega aca quiere decir q ya se valido
        return ProductoService().bajaProducto(id_producto)

class ArchivoProducto(Resource):
    def post(self,id_producto):
        archivo = request.files['detallesTecnicos']
        if(archivo):
            return ProductoService().asociarArchivo(archivo,id_producto)
        return {'name': 'None'},400