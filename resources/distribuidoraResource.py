from servicios.distribuidoraService import DistribuidoraService
from flask_restful import Resource,Api
from flask_jwt import jwt_required
from flask import request



class DistribuidoraResource(Resource):
    def post(self):
        datos = request.get_json()
        if(datos):
            return DistribuidoraService().altaDistribuidora(datos)
        return {'name': 'None'},400

    def put(self):
        datos = request.get_json()
        if(datos):
            return DistribuidoraService().modificarDistribuidora(datos)
        return {'name': 'None'},400
    
    def delete(self):
        #ver: borramos el producto ¿que sucede con los productos activos en stock?
        datos = request.get_json()
        if(datos):
            return DistribuidoraService().bajaDistribuidora(datos)
        return {'name': 'None'},400
    
class ObtenerDistribuidorasResource(Resource):
    def get(self):
        return DistribuidoraService().obtenerDistribuidoras()
    
class ObtenerDistribuidoraResource(Resource):
    def get(self,id_distribuidora):
        return DistribuidoraService().obtenerDistribuidora(id_distribuidora)

     