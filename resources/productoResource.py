from servicios.productoService import ProductoService
from flask_restful import Resource,Api
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
    

    def delete(self):
        #ver: borramos el producto ¿que sucede con los productos activos en stock?
        datos = request.get_json()
        if(datos):
            return ProductoService().bajaProducto(datos)
        return {'name': 'None'},400
    
class ObtenerProductosResource(Resource):
    def get(self):
        return ProductoService().obtenerProductos()
    
class ObtenerProductoResource(Resource):
    def get(self,id_producto):
        return ProductoService().obtenerProducto(id_producto)

     