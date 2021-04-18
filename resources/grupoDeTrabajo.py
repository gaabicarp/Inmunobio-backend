from db import dbMongo
from marshmallow import Schema, fields, post_load, ValidationError
from bson import ObjectId
from dateutil import parser
from flask import jsonify
import json
from models.mongo.grupoDeTrabajo import GrupoDeTrabajoSchema,GrupoDeTrabajo
from flask_restful import Resource, Api
from flask import jsonify, request
from servicios.GrupoDeTrabajoService import GrupoDeTrabajoService
 
class NuevoGrupoDeTrabajo(Resource):
        def post(self):
            datos = request.get_json()
            if datos:
                try:
                    grupoCreado = GrupoDeTrabajoSchema().load(datos)
                    grupoCreado.save()
                    return {'Status':'ok'},200
                except ValidationError as err:
                    return {'error': err.messages},404
            return {'name': datos},404

class MiembrosGrupoDeTrabajo(Resource):
    def put(self,id):
            #edita miembros de un grupo de trabajo, esta accion solo puede realizarla el jefe del grupo.
            #recibe id por parametro y miembros por json.
            # to-do: ver si es necesario pasar todo x json
            datos = request.get_json()
            if datos:
                grupoAModif = GrupoDeTrabajoService.find_by_id(id)
                if (grupoAModif):
                        GrupoDeTrabajoService.modificarMiembros(id,datos,grupoAModif)
                        return {'Status':'ok'},200   
                return  {'error':'El grupo de trabajo no existe'},404
            return {'name': datos},404

class GrupoDeTrabajoPorId(Resource):
   
    def get(self,id):
        #dado un id de grupo de trabajo devuelve todos los datos del grupo de GrupoDeTrabajo si lo encuentra
        grupoConsulta= GrupoDeTrabajoService.find_by_id(id)
        if (grupoConsulta):
            return GrupoDeTrabajoService.json(grupoConsulta)
        return  {'error':'El grupo de trabajo no existe'},404    
