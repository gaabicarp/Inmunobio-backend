from db import dbMongo
from flask_restful import Resource
from flask import request
from servicios.grupoDeTrabajoService import GrupoDeTrabajoService

class RenombrarJefeGrupo(Resource):
    def put(self):
            datos = request.get_json()
            if datos:
                return GrupoDeTrabajoService.modificarJefeGrupo(datos)
            return {'name': 'None'},400

class GrupoDeTrabajo(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            return GrupoDeTrabajoService.nuevoGrupo(datos)
        return {'name': 'None'},400

    def put(self):
        datos = request.get_json()
        if datos:
            return GrupoDeTrabajoService.modificarMiembrosGrupo(datos)
        return {'name': 'None'},400

class GrupoDeTrabajoID(Resource):
    def get(self,id_grupoDeTrabajo):        
        return GrupoDeTrabajoService.obtenerGrupoPorId(id_grupoDeTrabajo)
    def delete(self,id_grupoDeTrabajo):
        return GrupoDeTrabajoService.removerGrupo(id_grupoDeTrabajo)

class GruposDeTrabajo(Resource):
    def get(self):
        return GrupoDeTrabajoService.obtenerTodosLosGrupos()



