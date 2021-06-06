from marshmallow import ValidationError
from models.mongo.espacioFisico import EspacioFisico
from schemas.espacioFisicoSchema import NuevoEspacioFisicoSchema,ModificarEspacioFisico,NuevoBlogEspacioFisicoSchema
from exceptions.exception import ErrorEspacioFisicoInexistente,ErrorBlogInexistente
from servicios.blogService import BlogService
from servicios.commonService import CommonService

class EspacioFisicoService():
    @classmethod
    def obtenerEspacios(cls):
        return EspacioFisico.objects.all()

    @classmethod
    def altaEspacioFisico(cls,datos):
            espacioNuevo=NuevoEspacioFisicoSchema().load(datos)
            espacioNuevo.save()

   
    @classmethod
    def find_by_id(cls,id):
        producto =  EspacioFisico.objects(id_espacioFisico = id).first()
        if(not producto):
            raise ErrorEspacioFisicoInexistente(id)
        return producto     

    @classmethod
    def modificarEspacio(cls,datos):
            ModificarEspacioFisico().load(datos)
            espacio = cls.find_by_id(datos['id_espacioFisico'])
            CommonService.updateAtributes(espacio,datos,'blogs')
            espacio.save()
   
    
    @classmethod
    def borrarEspacio(cls,id_espacioFisico):
            espacio = cls.find_by_id(id_espacioFisico)
            espacio.delete()

    @classmethod
    def crearBlogEspacioFisico(cls,datos):
            NuevoBlogEspacioFisicoSchema().load(datos)
            espacio = cls.find_by_id(datos['id_espacioFisico'])
            blog = BlogService.nuevoBlog(datos['blogs'])
            espacio.blogs.append(blog)
            espacio.save()


    @classmethod
    def obtenerBlogs(cls,id_espacioFisico):
        espacio = cls.find_by_id(id_espacioFisico)
        return espacio.blogs


    @classmethod
    def BorrarBlogEspacioFisico(cls,_id_espacioFisico,_id_blog):
            if(EspacioFisico.objects.filter(id_espacioFisico = _id_espacioFisico).first()):
                if (EspacioFisico.objects.filter(id_espacioFisico = _id_espacioFisico, blogs__id_blog= _id_blog).first()):
                    return EspacioFisico.objects.filter(id_espacioFisico = _id_espacioFisico).first().modify(pull__blogs__id_blog =_id_blog)
                raise ErrorBlogInexistente(_id_blog)
            raise ErrorEspacioFisicoInexistente(_id_espacioFisico)

 


