from servicios.distribuidoraService import DistribuidoraService
from flask_restful import Resource,Api
from flask_jwt import jwt_required
from flask import request
from marshmallow import ValidationError
from exceptions.exception import ErrorDistribuidoraInexistente
from servicios.commonService import CommonService
from schemas.distribuidoraSchema import DistribuidoraSchema

class DistribuidoraResource(Resource):
    def post(self):
        datos = request.get_json()
        if(datos):
            try:
                DistribuidoraService().altaDistribuidora(datos)
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'error': err.messages},400
        return {'name': 'None'},400

    def put(self):
        datos = request.get_json()
        if(datos):
            try:
                DistribuidoraService().modificarDistribuidora(datos)
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'error': err.messages},400
            except ErrorDistribuidoraInexistente as err:
                return {'Error': err.message},400
        return {'name': 'None'},400
    
class ObtenerDistribuidorasResource(Resource):
    def get(self):
        return DistribuidoraService().obtenerDistribuidoras()
    
class DistribuidoraID(Resource):
    def get(self,id_distribuidora):
        try:
            distribuidora = DistribuidoraService().find_by_id(id_distribuidora)
            return CommonService.json(distribuidora,DistribuidoraSchema)
        except ErrorDistribuidoraInexistente as err:
            return {'Error': err.message},400
    
    def delete(self,id_distribuidora):
        #ver: borramos el producto ¿que sucede con los productos activos en stock?
        #se da de baja!!
        try:
            #valida si existe producto activo con esta id?
            DistribuidoraService().bajaDistribuidora(id_distribuidora)
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400
        except ErrorDistribuidoraInexistente as err:
          return {'Error': err.message},400

     