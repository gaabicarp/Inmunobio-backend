from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from servicios.commonService import CommonService
from servicios.muestraService import MuestraService
from schemas.muestraSchema import  MuestraSchema

class Muestra(Resource):
    def get(self, idMuestra):
        if idMuestra:
            try:
                return CommonService.json(MuestraService().find_by_id(idMuestra),MuestraSchema)
            except Exception as err:
                return {'Error': err.args}, 400
        return {"Error" : "Se debe indicar el id de la muestra."}, 400

    def post(self):
        datos = request.get_json()
        if datos:
            try:
                MuestraService().nuevasMuestras(datos)
                return {'Status': 'Muestra creada'}, 200
            except Exception as err:
                return {'Error': err.args}, 400 
        return {'Error': "Se deben enviar datos para crear la muestra"}, 400

    def put(self):
        datos = request.get_json()
        if datos:
            try:
                MuestraService().modificarMuestra(datos)
                return {'Status': 'Se modificó la muestra'}, 200
            except Exception as err:
                return {'Error': err.args}, 400
        return {'Error': "Se deben enviar datos para modificar la muestra"}, 400

    def delete(self, idMuestra):
        if idMuestra:
            try:
                MuestraService().darDeBajaMuestra(idMuestra)
                return {"Status": f"Se dio de baja la muestra con id {idMuestra}"}, 200
            except Exception as err:
                return {'Error': err.args}, 400
        return {"Error" : "Se debe indicar el id de la muestra."}, 400

class MuestraGrupoExperimental(Resource):
    def get(self, idGrupoExperimental):
        if idGrupoExperimental:
            try:
                return CommonService.jsonMany(MuestraService().find_all_by_grupoExperimental(idGrupoExperimental),MuestraSchema)
            except Exception as err:
                return {'Error': err.args}, 400
        return {'Error' : "Se deben enviar un id del grupo experimental válido."}, 400

class MuestraProyecto(Resource):
    def get(self, idProyecto):
        if idProyecto:
            try:
                return CommonService.jsonMany(MuestraService().find_all_by_proyecto(idProyecto),MuestraSchema)
            except Exception as err:
                return {'Error': err.args}, 400
        return {'Error' : "Se deben enviar un id de proyecto válido."}, 400

class MuestraExperimento(Resource):
    def put(self):
        datos = request.get_json()
        if datos:
            MuestraService().agregarMuestrasExternasAlExperimento(datos)

class MuestrasPorIDFuente(Resource):
    def get(self,idFuenteExperimental):
        if idFuenteExperimental :
            return MuestraService().obtenerMuestrasDeFuente(idFuenteExperimental)
        return {'Error' : "Se deben enviar un id de fuente ."}, 400

class BorraMuestras(Resource):
    def post(self):
        from models.mongo.muestra import Muestra
        Muestra.objects.delete()