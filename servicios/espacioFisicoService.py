from marshmallow import ValidationError
from models.mongo.espacioFisico import EspacioFisico
from schemas.espacioFisicoSchema import NuevoEspacioFisicoSchema,ModificarEspacioFisico,EspacioFisicoSchema
from exceptions.exception import ErrorEspacioFisicoInexistente
from servicios.commonService import CommonService


class EspacioFisicoService():
    @classmethod
    def altaEspacioFisico(cls,datos):
        try:
            espacioNuevo=NuevoEspacioFisicoSchema().load(datos)
            espacioNuevo.save()
            return {'Status':'ok'},200
        except ValidationError as err:
                return {'error': err.messages},400 
        #except (ErrorProductoEnStockInexistente,ErrorStockInexistente) as err:
        #       return {'Error':err.message},400 
        #  
    @classmethod
    def find_by_id(cls,id):
        producto =  EspacioFisico.objects(id_espacioFisico = id).first()
        if(not producto):
            raise ErrorEspacioFisicoInexistente(id)
        return producto     

    @classmethod
    def modificarEspacio(cls,datos):
        try:
            ModificarEspacioFisico().load(datos)
            espacio = cls.find_by_id(datos['id_espacioFisico'])
            CommonService.updateAtributes(espacio,datos,'blogs')
            espacio.save()
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400 
        except ErrorEspacioFisicoInexistente as err:
            return {'error':err.message},400

    @classmethod
    def obtenerEspacio(cls,id_espacioFisico):
        try:
            espacio = cls.find_by_id(id_espacioFisico)
            return CommonService.json(espacio,EspacioFisicoSchema)
        except ValidationError as err:
            return {'error': err.messages},400 
        except ErrorEspacioFisicoInexistente as err:
            return {'error':err.message},400


    @classmethod
    def borrarEspacio(cls,id_espacioFisico):
        try:
            espacio = cls.find_by_id(id_espacioFisico)
            espacio.delete()
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400 
        except ErrorEspacioFisicoInexistente as err:
            return {'error':err.message},400

    @classmethod
    def crearBlogEspacioFisico(cls,datos):
        try:
            espacio = cls.find_by_id(datos['id_espacioFisico'])
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400 
        except ErrorEspacioFisicoInexistente as err:
            return {'error':err.message},400

    @classmethod
    def BorrarBlogEspacioFisico(cls,id_espacioFisico,_id_blog):
        try:
            espacio = cls.find_by_id(id_espacioFisico)
            return espacio.update(pull__id_blog = _id_blog),200
            #return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400 
        except ErrorEspacioFisicoInexistente as err:
            return {'error':err.message},400
                 





