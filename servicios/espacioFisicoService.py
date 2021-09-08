from marshmallow import ValidationError
from models.mongo.espacioFisico import EspacioFisico
from schemas.espacioFisicoSchema import BusquedaBlogEspacio,NuevoEspacioFisicoSchema,ModificarEspacioFisico,NuevoBlogEspacioFisicoSchema
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
    def obtenerNombreEspacioFisico(cls,id):
        return cls.find_by_id(id).nombre
   
    @classmethod
    def find_by_id(cls,id):
        espacio =  EspacioFisico.objects(id_espacioFisico = id).first()
        if(not espacio):
            raise Exception(f"No existe espacio fisico con id {id}")
        return espacio     

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
    def obtenerBlogs(cls,datos):
        BusquedaBlogEspacio().load(datos)
        espacio = cls.find_by_id(datos['id_espacioFisico'])
        return BlogService.busquedaPorFecha(espacio.blogs,datos['fechaDesde'],datos['fechaHasta'])

    @classmethod
    def BorrarBlogEspacioFisico(cls,_id_espacioFisico,_id_blog):
        #TO-DO ; arreglar este codigo 
        if(EspacioFisico.objects.filter(id_espacioFisico = _id_espacioFisico).first()):
            if (EspacioFisico.objects.filter(id_espacioFisico = _id_espacioFisico, blogs__id_blog= _id_blog).first()):
                return EspacioFisico.objects.filter(id_espacioFisico = _id_espacioFisico).first().modify(pull__blogs__id_blog =_id_blog)
            raise Exception(f"No se encontró ningun blog con el id: {_id_blog}")
        raise Exception(f"No existe espacio fisico con id {_id_espacioFisico}")
 

