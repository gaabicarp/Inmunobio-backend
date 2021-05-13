from flask_restful import Resource,Api
from flask_jwt import jwt_required
from flask import request
from dateutil import parser
from servicios.stockService import  StockService

class NuevoProductoEnStock(Resource):
    def post(self):
        """Recibe un json con id_grupoDeTrabajo,lote(opc), detalleUbicacion(opc)
        unidad (x default 1) fechaVencimiento(opc) id_espacioFisico(obligatorio),codigoContenedor(opc) e id de producto (obligatorio)"""
        datos = request.get_json()
        if(datos):
            return StockService.nuevoStock(datos)
        return {'name': 'None'},400

class ProductoEnStock(Resource):
    def delete(self):
        datos = request.get_json()
        if(datos):
            return StockService.borrarStock(datos)
        return {'name': 'None'},400


class ObtenerProductosStock(Resource):
    def get(self,id_grupoDeTrabajo):
            return StockService.obtenerProductos(id_grupoDeTrabajo)


