from db import dbMongo
#from marshmallow import Schema, fields, post_load, ValidationError
#from bson import ObjectId
#from dateutil import parser
#from flask import jsonify
import json
from models.mongo.grupoDeTrabajo import GrupoDeTrabajoSchema,GrupoDeTrabajo
from marshmallow import Schema, ValidationError
#from flask_restful import Resource,Api
from flask import jsonify, request

class GrupoDeTrabajoService:
    def find_by_id(id):
        return GrupoDeTrabajo.objects.filter(idGrupoDeTrabajo=id).first()

    def find_by_nombre(_nombre):
        return GrupoDeTrabajo.objects(nombre = _nombre).first()
    
    def modificarGrupo(datos,grupoAModificar):
        #Si se pasa una lista de los nuevos miembros, y se pisa la anterior 
        if 'integrantes' in datos.keys():
            grupoAModificar.update(integrantes=datos['integrantes'])
        if 'jefeDeGrupo' in datos.keys():
            grupoAModificar.update(jefeDeGrupo=datos['jefeDeGrupo'])
       
    def json(datos):
        return GrupoDeTrabajoSchema().dump(datos)

    def jsonMany(datos):
        return jsonify(GrupoDeTrabajoSchema().dump(datos,many=True))
    def removerGrupo(grupo):
        #falta ver que pasa con los roles de un jefe cuando se borra el grupo 
        return grupo.delete()

    def obtenerTodosLosGrupos():
        return GrupoDeTrabajo.objects.all()
    def nuevoGrupo(datos):
            grupoCreado = GrupoDeTrabajoSchema().load(datos)
            grupoCreado.save()
            return grupoCreado
            