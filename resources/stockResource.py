from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from servicios.stockService import  StockService

class ProductoEnStock(Resource):
    def post(self):
        """Recibe un json con id_grupoDeTrabajo,lote(opc), detalleUbicacion(opc)
        unidad (x default 1) fechaVencimiento(opc) id_espacioFisico(obligatorio),codigoContenedor(opc) e id de producto (obligatorio)"""
        datos = request.get_json()
        if(datos):
            return StockService.nuevoStock(datos)
        return {'name': 'None'},400

    def put(self):
        datos = request.get_json()
        if(datos):
            return StockService.modificarProductoEnStock(datos)
        return {'name': 'None'},400

class ObtenerProductosStock(Resource):
    def get(self,id_grupoDeTrabajo,id_espacioFisico):
        return StockService.obtenerProductos(id_grupoDeTrabajo,id_espacioFisico)
    
class BorrarTodoStock(Resource):
    def delete(self,id_grupoDeTrabajo):
        return StockService.borrarTodo(id_grupoDeTrabajo)

class ProductoEnStockID(Resource):
    def delete(self,id_productoEnStock,id_productos):
        return StockService.borrarProductoEnStock(id_productoEnStock,id_productos)
    
class ConsumirStockResource(Resource):
    def put(self):
        datos = request.get_json()
        if(datos):
            return StockService.consumirStock(datos)
        return {'name': 'None'},400

        
        
