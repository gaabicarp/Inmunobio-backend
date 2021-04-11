from db import dbMongo
from marshmallow import Schema, fields, post_load, ValidationError
from bson import ObjectId
from dateutil import parser
from flask import jsonify
from models.mysql.usuario import Usuario
import json
from models.mongo.grupoDeTrabajo import GrupoDeTrabajoSchema,GrupoDeTrabajo
from flask_restful import Resource,Api
from flask import jsonify, request


 
class NuevoGrupoDeTrabajo(Resource):
        def post(self):
            datos = request.get_json()
            if datos:
                schemaGrupo = GrupoDeTrabajoSchema()
                try:
                    grupoCreado = schemaGrupo.load(datos)
                    grupoCreado.save()
                    return {'Status':'ok'},200
                except ValidationError as err:
                    return {'error': err.messages},404
            return {'name': datos},404


class GrupoDeTrabajoPorId(Resource):
    def put(self,id):
        #edita miembros o jefe de grupo
        datos = request.get_json()
        if datos:
            if('id' in datos ):
                grupoAModificar = GrupoDeTrabajo.find_by_id(datos['id'])
                if (grupoAModificar):
                    GrupoDeTrabajo.modificarMiembros(datos)
                    return {'Status':'ok'},200   
                return  {'error':'El grupo de trabajo no existe'},404
            return {'error':'No se envio la id'},404
        return {'name': datos},404

    def get(self,id):
        #obtiene grupo de trabajo mediante id
        #datos = request.get_json()
        #if datos:
        #if('id' in datos ):
        grupoConsulta= GrupoDeTrabajo().find_by_id(id)
        if (grupoConsulta):
                return grupoConsulta.json()
        return  {'error':'El grupo de trabajo no existe'},404
                
        #return {'error':'No se envio la id'},404
        return {'name': datos},404
