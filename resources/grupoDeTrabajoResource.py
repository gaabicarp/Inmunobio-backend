from db import dbMongo
from marshmallow import Schema,  ValidationError
from models.mongo.grupoDeTrabajo import GrupoDeTrabajoSchema,GrupoDeTrabajo
from flask_restful import Resource,Api
from flask import request
from servicios.grupoDeTrabajoService import GrupoDeTrabajoService
 
class NuevoGrupoDeTrabajo(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            return GrupoDeTrabajoService.nuevoGrupo(datos)
        return {'name': datos},404


class GruposDeTrabajo(Resource):
    def get(self):
        #ok
        gruposConsulta= GrupoDeTrabajoService.obtenerTodosLosGrupos()
        if(gruposConsulta):
            return GrupoDeTrabajoService.jsonMany(gruposConsulta)
        return  {'error':'No existen grupos de trabajo '},404     

class RenombrarJefeGrupo(Resource):
    def put(self):
        #ok
            '''edita jefe de grupo de trabajo, esta accion solo puede realizarla usuario nivel 2.
            recibe id de grupo e id de jefe nuevo por json'''
            datos = request.get_json()
            if datos:
                return GrupoDeTrabajoService.modificarJefeGrupo(datos)
            return {'name': datos},404

class GrupoDeTrabajo(Resource):
    def put(self):
        #ok
        '''edita miembros de un grupo de trabajo, esta accion solo puede realizarla el jefe del grupo.
        recibe id de grupo y miembros por json.'''
        datos = request.get_json()
        if datos:
            return GrupoDeTrabajoService.modificarMiembrosGrupo(datos)
        return {'name': datos},404

    def get(self):
        #ok
        #dado un id de grupo de trabajo devuelve todos los datos del grupo de GrupoDeTrabajo si lo encuentra
        datos = request.get_json()
        if (datos):
            return GrupoDeTrabajoService.obtenerGrupoPorId(datos)
        return {'name': datos},404

    def delete(self):
        datos = request.get_json()
        if (datos):
            return GrupoDeTrabajoService.removerGrupo(datos)
        return {'name': datos},404        
