from dateutil import parser
import datetime
from models.mongo.proyecto import Proyecto
from schemas.proyectoSchema import NuevoBlogProyectoSchema,ObtenerBlogsProyectoSchema, ProyectoCerradoSchema, ProyectoModificarSchema,ProyectoNuevoSchema
from servicios.usuarioService import UsuarioService
from exceptions.exception import ErrorProyectoInexistente
from servicios.blogService import BlogService

class ProyectoService:
    @classmethod
    def find_all(cls):
        return Proyecto.objects.filter().all()
        
    @classmethod
    def find_by_id(cls, id):
        proyecto =  Proyecto.objects.filter(id_proyecto=id).first()
        if not proyecto: raise ErrorProyectoInexistente(id)
        return proyecto

    @classmethod
    def nuevoProyecto(cls, datos):
        proyecto = ProyectoNuevoSchema().load(datos)
        UsuarioService.busquedaUsuariosID(datos['participantes']) #validamos que se pasen usuarios validos 
        proyecto.save()

    @classmethod
    def find_by_nombre(cls, _nombre):
        return Proyecto.objects(nombre = _nombre).first()
    
    @classmethod
    def cerrarProyecto(cls, datos):
        proyecto = ProyectoCerradoSchema().load(datos)
        Proyecto.objects(id_proyecto = proyecto.id_proyecto).update(
            conclusion = proyecto.conclusion,
            finalizado = True,
            fechaFinal = parser.parse(str(datetime.datetime.utcnow()))
        )
    
    #Agregar modificar Participantes
    @classmethod
    def modificarProyecto(cls, datos):
        proyecto = ProyectoModificarSchema().load(datos)
        if proyecto.descripcion.strip() != "":
            Proyecto.objects(id_proyecto = proyecto.id_proyecto).update(set__descripcion = proyecto.descripcion)
        Proyecto.objects(id_proyecto = proyecto.id_proyecto).update(set__montoInicial = proyecto.montoInicial)
    
    @classmethod
    def agregarMiembros(cls):
        usuariosIdPermitidas = UsuarioService.UsuarioService()
        return usuariosIdPermitidas

    @classmethod
    def obtenerMiembrosProyecto(cls, id_proyecto):    
        proyecto = cls.find_by_id(id_proyecto)
        return UsuarioService.busquedaUsuariosID(proyecto.participantes)

    @classmethod
    def obtenerBlogsProyecto(cls,datos):
        ObtenerBlogsProyectoSchema().load(datos)
        proyecto = cls.find_by_id(datos['id_proyecto'])
        return BlogService.blogsProyecto(proyecto.id_proyecto,datos['fechaDesde'],datos['fechaHasta'])
        
    @classmethod
    def nuevoBlogsProyecto(cls,datos):
        datosBlog = NuevoBlogProyectoSchema().load(datos)
        print(datosBlog)
        if cls.esBlogJaula(datosBlog['blogs']):
            from servicios.jaulaService import JaulaService
            JaulaService.crearBlogJaula(datos['id'],datos['blogs'])
        else: print('soy blog de exp')
        
    

    @classmethod
    def esBlogJaula(cls,blog):
        return blog.tipo == "Jaula"

