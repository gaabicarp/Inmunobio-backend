from db import dbMongo
from flask_restful import Resource,Api
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

    def delete(self):
        datos = request.get_json()
        if (datos):
            return GrupoDeTrabajoService.removerGrupo(datos)
        return {'name': 'None'},400


class ObtenerGrupoDeTrabajo(Resource):
    def get(self,id_grupoDeTrabajo):        
        datos = request.get_json()
        if (datos):
            return GrupoDeTrabajoService.obtenerGrupoPorId(id_grupoDeTrabajo)
        return {'name': 'None'},400


class GruposDeTrabajo(Resource):
    def get(self):
        gruposConsulta= GrupoDeTrabajoService.obtenerTodosLosGrupos()
        if(gruposConsulta):
            return GrupoDeTrabajoService.jsonMany(gruposConsulta)

        return{'error':'No existen grupos de trabajo '},400


