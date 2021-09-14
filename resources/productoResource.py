from servicios.productoService import ProductoService
from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request,jsonify
from schemas.grupoTrabajoSchema import GrupoDeTrabajoSchema
from servicios.commonService import CommonService

class ProductoResource(Resource):
    def post(self):
        datos = request.get_json()
        if(datos):
            try:
                return ProductoService().altaProducto(datos),200
            except Exception as err:
                return {'Error': err.args},400 
        return {'Error': 'Deben indicarse datos para el alta del producto'},400

    def put(self):
        datos = request.get_json()
        if(datos):
            try:
                ProductoService().modificarProducto(datos)
                return {'Status':'Se modificó el producto.'},200
            except Exception as err:
                return {'Error': err.args},400 
        return {'Error': 'Deben indicarse datos para modificar el producto'},400

class ObtenerProductosResource(Resource):
    def get(self):
        return jsonify(ProductoService.obtenerProductos())
    
class ProductoID(Resource):
    def get(self,id_producto):
        if(id_producto):
            try:
                return ProductoService().obtenerProducto(id_producto)
            except Exception as err:
                return {'Error': err.args},400 
        return {'Error': 'Debe indicarse id_producto'},400

    def delete(self,id_producto):
        if(id_producto):
            try:
                ProductoService().bajaProducto(id_producto)
                return {'Status':'Se dio de baja el producto correctamente.'},200
            except Exception as err:
                return {'Error': err.args},400  
        return {'Error': 'Debe indicarse id_producto'},400

class ArchivoProducto(Resource):
    def post(self,id_producto):
        archivo = request.files['detallesTecnicos']
        if(archivo):
            try:
                ProductoService().asociarArchivo(archivo,id_producto)
                return {'Status':'Se asoció el archivo al producto.'} ,200
            except Exception as err:
                return {'Error': err.args},400  
        return {'Error': 'Debe subirse el archivo correspondiente al campo detallesTecnicos'},400

class ProductoEnStockDeGrupos(Resource):
    def get(self,id_producto):
        if(id_producto):
            try:
                return CommonService.jsonMany(ProductoService().getGruposByProducto(id_producto),GrupoDeTrabajoSchema)
            except Exception as err:
                return {'Error': err.args},400  
        return {'Error': 'Debe indicarse id producto'},400