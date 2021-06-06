from marshmallow import ValidationError
from models.mongo.espacioFisico import EspacioFisico
from schemas.espacioFisicoSchema import NuevoEspacioFisicoSchema,ModificarEspacioFisico,EspacioFisicoSchema,NuevoBlogEspacioFisicoSchema
from exceptions.exception import ErrorEspacioFisicoInexistente,ErrorBlogInexistente
from servicios.commonService import CommonService
from servicios.blogService import BlogService

class EspacioFisicoService():


    @classmethod
    def obtenerEspacios(cls):
        return CommonService.jsonMany(EspacioFisico.objects.all(),EspacioFisicoSchema)

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
            NuevoBlogEspacioFisicoSchema().load(datos)
            espacio = cls.find_by_id(datos['id_espacioFisico'])
            blog = BlogService.nuevoBlog(datos['blogs'])
            espacio.blogs.append(blog)
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400 
        except ErrorEspacioFisicoInexistente as err:
            return {'error':err.message},400

    @classmethod
    def BorrarBlogEspacioFisico(cls,_id_espacioFisico,_id_blog):
        try:
            if(EspacioFisico.objects.filter(id_espacioFisico = _id_espacioFisico).first()):
                if (EspacioFisico.objects.filter(id_espacioFisico = _id_espacioFisico, blogs__id_blog= _id_blog).first()):
                    EspacioFisico.objects.filter(id_espacioFisico = _id_espacioFisico).first().modify(pull__blogs__id_blog =_id_blog)
                    return {'Status':'ok'},200
                raise ErrorBlogInexistente(_id_blog)
            raise ErrorEspacioFisicoInexistente(_id_espacioFisico)
        except ErrorEspacioFisicoInexistente as err:
            return {'error':err.message},400
                 
 


