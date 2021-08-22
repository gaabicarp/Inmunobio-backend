from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from servicios.stockService import  StockService
from marshmallow import EXCLUDE

class ProductoEnStock(Resource):
    def post(self):
        datos = request.get_json()
        if(datos):
            try:
                StockService.nuevoStock(datos)
                return {'Status':'Se creo el producto en stock.'},200
            except Exception as err:
                 return {'Error': err.args},400  
        return {'Error':'Deben suministrarse datos para el alta del stock.'},400

    def put(self):
        datos = request.get_json()
        if(datos):
            try:
                StockService.modificarProductoEnStock(datos)
                return {'Status':'Se modifico el stock'},200
            except Exception as err:
                return {'Error': err.args},400  
        return {'Error': 'Deben suministrarse datos para la modificacion del producto en stock.'},400

class ObtenerProductosStock(Resource):
    def get(self,id_grupoDeTrabajo,id_espacioFisico):
        try:
            return  StockService.obtenerProductos(id_grupoDeTrabajo,id_espacioFisico)
        except Exception as err:
            return {'Error': err.args},400  

class BorrarTodoStock(Resource):
    def delete(self,id_grupoDeTrabajo):
        return StockService.borrarTodo(id_grupoDeTrabajo)

class ProductoEnStockID(Resource):
    def delete(self,id_productoEnStock,id_productos):
        try:
            StockService.borrarProductoEnStock(id_productoEnStock,id_productos)           
            return {'Status':'Se borró el producto en stock.'},200
        except Exception as err:
            return {'Error': err.args},400  

class ConsumirStockResource(Resource):
    def put(self):
        datos = request.get_json()
        if(datos):
            try:
                StockService.consumirStock(datos)
                return {'Status':'Se modificaron las unidades del producto en stock.'},200
            except Exception as err:
                return {'Error': err.args},400  
        return {'Error': 'Deben suministrarse los datos para modificar unidades en stock'},400 