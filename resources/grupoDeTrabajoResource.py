from db import dbMongo
from flask_restful import Resource
from flask import request
from servicios.grupoDeTrabajoService import GrupoDeTrabajoService
from servicios.commonService import CommonService
from schemas.grupoTrabajoSchema import GrupoDeTrabajoDatosExtra

class GrupoDeTrabajo(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                GrupoDeTrabajoService.nuevoGrupo(datos)
                return {'Status':'Se creó el grupo.'},200  
            except Exception as err:
                return {'Error': err.args},400
        return {'Error': 'Debe suministrar datos para el alta del grupo de trabajo.'},400

    def put(self):
        datos = request.get_json()
        if datos: 
            try:
                GrupoDeTrabajoService.modificarGrupo(datos)
                return {'Status':'Se modificó el grupo.'},200  
            except Exception as err:
                return {'Error': err.args},400
        return {'Error': 'Debe suministrar datos para la modificacion del grupo de trabajo.'},400

class GrupoDeTrabajoID(Resource):
    def get(self,id_grupoDeTrabajo):  
        if(id_grupoDeTrabajo):
            try:
                return CommonService.json(GrupoDeTrabajoService.obtenerGrupoPorId(id_grupoDeTrabajo),GrupoDeTrabajoDatosExtra)
            except Exception as err:
                return {'Error': err.args},400
        return {'Error': 'Debe indicarse el id del grupo de trabajo.'},400

    def delete(self,id_grupoDeTrabajo):
        if(id_grupoDeTrabajo):
            try:
                GrupoDeTrabajoService.removerGrupo(id_grupoDeTrabajo)
                return {'Status':'Grupo eliminado.'},200
            except Exception as err:
                return {'Error': err.args},400
        return {'Error': 'Debe indicarse el id del grupo de trabajo.'},400

class GruposDeTrabajo(Resource):
    def get(self):
        return GrupoDeTrabajoService.obtenerTodosLosGrupos()

#en desuso
class RenombrarJefeGrupo(Resource):
    def put(self):
        datos = request.get_json()
        if datos:
            try:
                GrupoDeTrabajoService.modificarJefeGrupo(datos)
                return {'Status':'Se modificó el jefe de grupo'},200  
            except Exception as err:
                return {'Error': err.args},400
        return {'Error': 'Deben suministrarse datos para renombrar Jefe.'},400
