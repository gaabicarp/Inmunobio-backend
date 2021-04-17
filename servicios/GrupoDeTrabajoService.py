from db import dbMongo
#from marshmallow import Schema, fields, post_load, ValidationError
#from bson import ObjectId
#from dateutil import parser
#from flask import jsonify
import json
from models.mongo.grupoDeTrabajo import GrupoDeTrabajoSchema,GrupoDeTrabajo
#from flask_restful import Resource,Api
#from flask import jsonify, request

class GrupoDeTrabajoService:
    @classmethod
    def find_by_id(cls,id):
        return GrupoDeTrabajo.objects.filter(idGrupoDeTrabajo=id).first()

    @classmethod
    def find_by_nombre(cls,_nombre):
        return GrupoDeTrabajo.objects(nombre = _nombre).first()
 
    @classmethod
    def modificarGrupo(cls,id,datos,grupoAModificar):
        #Si se pasa una lista de los nuevos miembros, y se pisa la anterior 
        if 'integrantes' in datos.keys():
            grupoAModificar.update_one(integrantes=datos['integrantes'])
        if 'jefeDeGrupo' in datos.keys():
            grupoAModificar.update_one(jefeDeGrupo=datos['jefeDeGrupo'])
    @classmethod      
    def json(cls,informacion):
        return GrupoDeTrabajoSchema().dump(informacion)
  
  
