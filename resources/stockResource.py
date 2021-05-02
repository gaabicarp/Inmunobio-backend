from flask_restful import Resource,Api
from flask_jwt import jwt_required
from flask import jsonify, request
from dateutil import parser
import json
from marshmallow import ValidationError
from servicios.stockService import StockService

class NuevoStock(Resource):
    def post(self):
        """Recibe un json con id_grupoDeTrabajo,lote,  detalleUbicacion(opc)
        unidad (opc) fechaVencimiento(opc) id_espacioFisico ,codigoContenedor(opc)"""
        datos = request.get_json()
        if(datos):
            return StockService.altaStock(datos)
        return {'name': 'None'},404

class Stock(Resource):
    def get(self):
        datos = request.get_json()
        if(datos):
            return StockService.obtenerStock(datos)
        return {'name': 'None'},404 