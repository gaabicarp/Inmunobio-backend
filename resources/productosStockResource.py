from flask_restful import Resource,Api
from flask_jwt import jwt_required
from flask import request
from dateutil import parser
from servicios.productosStockService import  ProductosStockService

class NuevoStock(Resource):
    def post(self):
        """Recibe un json con id_grupoDeTrabajo,lote,  detalleUbicacion(opc)
        unidad (opc) fechaVencimiento(opc) id_espacioFisico(obligatorio),codigoContenedor(opc) e id de producto"""
        datos = request.get_json()
        if(datos):
            return ProductosStockService.altaProductoEnStock(datos)
        return {'name': 'None'},404

class ObtenerProductosStock(Resource):
    def get(self,id_grupoDeTrabajo):
            return ProductosStockService.obtenerProductos(id_grupoDeTrabajo)
