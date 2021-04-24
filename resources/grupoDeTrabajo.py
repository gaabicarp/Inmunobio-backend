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
            try:
                nuevoGrupo = GrupoDeTrabajoService.nuevoGrupo(datos)
                return {'Status':'ok'},200  
            except ValidationError as err:
                return {'error': err.messages},400
        return {'name': datos},404



class GruposDeTrabajo(Resource):
    def get(self):
        gruposConsulta= GrupoDeTrabajoService.obtenerTodosLosGrupos()
        if(gruposConsulta):
            return GrupoDeTrabajoService.jsonMany(gruposConsulta)
        return  {'error':'No existen grupos de trabajo '},404     

class GrupoDeTrabajo(Resource):
    def put(self,id):
        #edita miembros de un grupo de trabajo, esta accion solo puede realizarla el jefe del grupo.
        #recibe id por parametro y miembros por json.
        # to-do: ver si es necesario pasar todo x json
        datos = request.get_json()
        if datos:
            grupoAModif = GrupoDeTrabajoService.find_by_id(id)
            if (grupoAModif):
                GrupoDeTrabajoService.modificarGrupo(datos,grupoAModif)
                return {'Status':'ok'},200   
            return  {'error':'El grupo de trabajo no existe'},404
        return {'name': datos},404

    def get(self,id):
        #dado un id de grupo de trabajo devuelve todos los datos del grupo de GrupoDeTrabajo si lo encuentra
        grupoConsulta= GrupoDeTrabajoService.find_by_id(id)
        if (grupoConsulta):
            return GrupoDeTrabajoService.json(grupoConsulta)
        return  {'error':'El grupo de trabajo no existe'},404    

    def delete(self,id):
        grupoABorrar = GrupoDeTrabajoService.find_by_id(id)
        if (grupoABorrar):
            return GrupoDeTrabajoService.removerGrupo(grupoABorrar)
        return  {'error':'El grupo de trabajo no existe'},404    
        
