from marshmallow import ValidationError
from flask import jsonify
from models.mongo.distribuidora import Distribuidora
from schemas.distribuidoraSchema import DistribuidoraSchema,NuevaDistribuidoraSchema,IdDistribuidoraSchema
from exceptions.exception import ErrorDistribuidoraInexistente
from servicios.commonService import CommonService

class DistribuidoraService():
    @classmethod
    def altaDistribuidora(cls,datos):
        try:
            nuevaDistribuidora = NuevaDistribuidoraSchema().load(datos)
            cls.validacionDistribuidora(datos)
            nuevaDistribuidora.save()
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400

    def validacionDistribuidora(datos):
        #debe validar algo la distribuidora?
        pass
    @classmethod    
    def find_by_id(cls,id):
        distribuidora =  Distribuidora.objects(id_distribuidora = id)
        if(not distribuidora):
            raise ErrorDistribuidoraInexistente()
        return distribuidora     

    @classmethod
    def bajaDistribuidora(cls,datos):
        try:
            #valida si existe producto activo con esta id?
            IdDistribuidoraSchema().load(datos)
            distribuidora = cls.find_by_id(datos['id_distribuidora'])
            distribuidora.delete()
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400
        except ErrorDistribuidoraInexistente as err:
          return {'Error': err.message},400

    def json(datos):
        return DistribuidoraSchema().dump(datos)

    def jsonMany(datos):
        return jsonify(DistribuidoraSchema().dump(datos,many=True))

    @classmethod
    def obtenerDistribuidoras(cls):
        return cls.jsonMany(Distribuidora.objects().all())

    @classmethod
    def modificarDistribuidora(cls,datos):
        try:
            NuevaDistribuidoraSchema().load(datos)
            distribuidora = cls.find_by_id(datos['id_distribuidora'])
            CommonService.updateAtributes(distribuidora,datos)
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400
        except ErrorDistribuidoraInexistente as err:
            return {'Error': err.message},400

    @classmethod        
    def obtenerDistribuidora(cls,id_distribuidora):
        try:
            distribuidora = cls.find_by_id(id_distribuidora)
            return cls.json(distribuidora)
        except ErrorDistribuidoraInexistente as err:
            return {'Error': err.message},400


        