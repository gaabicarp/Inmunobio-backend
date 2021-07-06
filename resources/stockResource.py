from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from servicios.stockService import  StockService
from marshmallow import ValidationError,EXCLUDE
from schemas.stockSchema import StockSchema
from exceptions.exception import ErrorGrupoInexistente,ErrorProductoInexistente,ErrorProductoEnStockInexistente,ErrorStockInexistente,ErrorUnidadStock,ErrorStockVacio,ErrorEspacioFisicoInexistente                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
from servicios.commonService import CommonService

class ProductoEnStock(Resource):
    def post(self):
        """Recibe un json con id_grupoDeTrabajo,lote(opc), detalleUbicacion(opc)
        unidad (x default 1) fechaVencimiento(opc) id_espacioFisico(obligatorio),codigoContenedor(opc) e id de producto (obligatorio)"""
        datos = request.get_json()
        if(datos):
            try:
                StockService.nuevoStock(datos)
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'error': err.messages},400
            except (ErrorGrupoInexistente,ErrorProductoInexistente,ErrorUnidadStock ,ErrorStockVacio,ErrorEspacioFisicoInexistente) as err:
                return {'error':err.message},400
        return {'Error':'Deben suministrarse datos para la alta'},400

    def put(self):
        datos = request.get_json()
        if(datos):
            try:
                StockService.modificarProductoEnStock(datos)
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'error': err.messages},400
            except (ErrorProductoEnStockInexistente,ErrorStockInexistente) as err:
                return {'Error':err.message},400 
        return {'Error': 'None'},400

class ObtenerProductosStock(Resource):
    def get(self,id_grupoDeTrabajo,id_espacioFisico):
        try:
            return  StockService.obtenerProductos(id_grupoDeTrabajo,id_espacioFisico)
        except ErrorGrupoInexistente as err:
            return {'Error':err.message},400

class BorrarTodoStock(Resource):
    def delete(self,id_grupoDeTrabajo):
        return StockService.borrarTodo(id_grupoDeTrabajo)

class ProductoEnStockID(Resource):
    def delete(self,id_productoEnStock,id_productos):
            try:
                StockService.borrarProductoEnStock(id_productoEnStock,id_productos)           
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'error': err.messages},400 
            except (ErrorProductoEnStockInexistente,ErrorStockInexistente) as err:
                return {'Error':err.message},400  

class ConsumirStockResource(Resource):
    def put(self):
        datos = request.get_json()
        if(datos):
            try:
                StockService.consumirStock(datos)
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'error': err.messages},400
            except (ErrorUnidadStock,ErrorStockInexistente,ErrorProductoEnStockInexistente) as err:
                return {'error': err.message},400
        return {'name': 'None'},400 