from servicios.distribuidoraService import DistribuidoraService
from flask_restful import Resource,Api
from flask_jwt import jwt_required
from flask import request
from servicios.commonService import CommonService
from schemas.distribuidoraSchema import DistribuidoraSchema

class DistribuidoraResource(Resource):
    def post(self):
        datos = request.get_json()
        if(datos):
            try:
                DistribuidoraService().altaDistribuidora(datos)
                return {'Status':'Se dió de alta la distribuidora.'},200
            except Exception as err:
                return {'Error': err.args}, 400
        return {'Error': 'Deben enviarse los datos para el alta de distribuidora.'},400

    def put(self):
        datos = request.get_json()
        if(datos):
            try:
                DistribuidoraService().modificarDistribuidora(datos)
                return {'Status': 'Se modificó la distribuidora.'},200
            except Exception as err:
                return {'Error': err.args},400
        return {'Error': 'Deben enviarse los datos para el modificacion de distribuidora.'},400
    
class ObtenerDistribuidorasResource(Resource):
    def get(self):
        return DistribuidoraService().obtenerDistribuidoras()
    
class DistribuidoraID(Resource):
    def get(self,id_distribuidora):
        try:
            distribuidora = DistribuidoraService().find_by_id(id_distribuidora)
            return CommonService.json(distribuidora,DistribuidoraSchema)
        except Exception as err:
            return {'Error': err.message},400
    
    def delete(self,id_distribuidora):
        if(id_distribuidora):
            try:
                DistribuidoraService().bajaDistribuidora(id_distribuidora)
                return {'Status':'Se eliminó la distribuidora'},200
            except Exception as err:
                return {'Error': err.args}, 400
        return {'Error': 'Debe indicarse id de distribuidora.'},400
     