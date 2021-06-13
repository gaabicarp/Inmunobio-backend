from marshmallow import ValidationError
from models.mongo.distribuidora import Distribuidora
from schemas.distribuidoraSchema import DistribuidoraSchema,ModificarDistribuidora,NuevaDistribuidoraSchema,IdDistribuidoraSchema
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
        distribuidora =  Distribuidora.objects(id_distribuidora = id).first()
        if(not distribuidora):
            raise ErrorDistribuidoraInexistente()
        return distribuidora  
           
    @classmethod
    def bajaDistribuidora(cls,id_distribuidora):
        try:
            #valida si existe producto activo con esta id?
            distribuidora = cls.find_by_id(id_distribuidora)
            distribuidora.delete()
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400
        except ErrorDistribuidoraInexistente as err:
          return {'Error': err.message},400
    @classmethod
    def obtenerDistribuidoras(cls):
        return CommonService.jsonMany(Distribuidora.objects().all(),DistribuidoraSchema)

    @classmethod
    def modificarDistribuidora(cls,datos):
        try:
            ModificarDistribuidora().load(datos)
            distribuidora = cls.find_by_id(datos['id_distribuidora'])
            CommonService.updateAtributes(distribuidora,datos,'id_distribuidora')
            distribuidora.save()
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400
        except ErrorDistribuidoraInexistente as err:
            return {'Error': err.message},400

    @classmethod        
    def obtenerDistribuidora(cls,id_distribuidora):
        try:
            distribuidora = cls.find_by_id(id_distribuidora)
            return CommonService.json(distribuidora,DistribuidoraSchema)
        except ErrorDistribuidoraInexistente as err:
            return {'Error': err.message},400
        