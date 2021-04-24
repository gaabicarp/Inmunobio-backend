from db import dbMongo
import json
from models.mongo.grupoDeTrabajo import GrupoDeTrabajoSchema,GrupoDeTrabajo
from marshmallow import Schema, ValidationError
from flask import jsonify, request

class GrupoDeTrabajoService:
    def find_by_id(id):
        return GrupoDeTrabajo.objects.filter(id_grupoDeTrabajo=id).first()

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

    
    def obtenerTodosLosGrupos():
        return GrupoDeTrabajo.objects.all()
        
    def nuevoGrupo(datos):
            grupoCreado = GrupoDeTrabajoSchema().load(datos)
            grupoCreado.save()
    @classmethod
    def removerGrupo(cls,grupo):
        #falta ver que pasa con los roles de un jefe cuando se borra el grupo 
        if(cls.validarDelete(grupo)):
            grupo.delete()
            return {'Status':'ok'},200
        return {'Status': 'El grupo no puede ser dado de baja por contener stock activo'}

    def validarDelete(grupo):
        return len(grupo.stock) == 0
              