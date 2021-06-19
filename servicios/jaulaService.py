from models.mongo.jaula import Jaula
from servicios.fuenteExperimentalService import FuenteExperimentalService
from servicios.blogService import BlogService
from exceptions.exception import ErrorJaulaInexistente,ErrorBlogInexistente,ErrorJaulaBaja
from schemas.jaulaSchema import  BusquedaBlogJaula,NuevaJaulaSchema, ActualizarProyectoJaulaSchema, ActualizarJaulaSchema,NuevoBlogJaulaSchema
from servicios.proyectoService import ProyectoService

class JaulaService:
    @classmethod
    def find_by_id(cls, idJaula):
        jaula =  Jaula.objects(id_jaula = idJaula).first()
        if not jaula: raise ErrorJaulaInexistente(idJaula)
        return jaula
    
    @classmethod
    def jaulasSinAsignar(cls):
        return Jaula.objects(id_proyecto = 0).all()
    
    @classmethod
    def jaulasDelProyecto(cls, idProyecto):
        return Jaula.objects(id_proyecto = idProyecto).all()

    @classmethod
    def crearJaula(cls, datos):
        jaula = NuevaJaulaSchema().load(datos)
        jaula.save()
    
    @classmethod
    def actualizarProyectoDeLaJaula(cls, datos):
        jaula = ActualizarProyectoJaulaSchema().load(datos)
        ProyectoService.find_by_id(jaula.id_proyecto)
        Jaula.objects(id_jaula = jaula.id_jaula).update(
            id_proyecto = jaula.id_proyecto
        )

    @classmethod
    def actualizarJaula(cls, datos):
        jaula = ActualizarJaulaSchema().dump(datos)
        Jaula.objects(id_jaula = jaula.id_jaula).update(
            codigo = jaula.codigo,
            rack = jaula.rack,
            estante = jaula.estante,
            capacidad = jaula.capacidad,
            tipo = jaula.tipo
        )
    
    @classmethod
    def bajarJaula(cls, idJaula):
        jaula = cls.find_by_id(idJaula)
        if cls.laJualaTieneAnimales(cls, idJaula): raise ErrorJaulaBaja()
        Jaula.objects(id_jaula = idJaula).update(habilitado = False)
        

    def laJualaTieneAnimales(self, idJaula):
        animales = FuenteExperimentalService.animalesDeLaJaula(idJaula)
        return  len(animales) > 0

    @classmethod
    def nuevoBlogJaula(cls, datos):
            NuevoBlogJaulaSchema().load(datos)
            cls.crearBlogJaula(cls,datos['id_jaula'],datos['blogs'])
            """ jaula = cls.find_by_id(datos['id_jaula'])
            blog = BlogService.nuevoBlog(datos['blogs'])
            jaula.blogs.append(blog)
            jaula.save() """
    
    @classmethod
    def crearBlogJaula(cls,id_jaula,datosBlog):
        jaula = cls.find_by_id(id_jaula)
        blog = BlogService.nuevoBlog(datosBlog)
        jaula.blogs.append(blog)
        jaula.save()

    @classmethod
    def borrarBlogJaula(cls,_id_jaula,_id_blog):
        if(Jaula.objects.filter(id_jaula = _id_jaula).first()):
            if (Jaula.objects.filter(id_jaula = _id_jaula, blogs__id_blog= _id_blog).first()):
                return Jaula.objects.filter(id_jaula = _id_jaula).first().modify(pull__blogs__id_blog =_id_blog)
            raise ErrorBlogInexistente(_id_blog)
        raise ErrorJaulaInexistente(_id_jaula)

    @classmethod
    def obtenerBlogs(cls,datos):
        BusquedaBlogJaula().load(datos)
        jaula = cls.find_by_id(datos['id_jaula'])
        return BlogService.busquedaPorFecha(jaula.blogs,datos['fechaDesde'],datos['fechaHasta'])



    @classmethod
    def obtenerJaulas(cls):
        jaulas =  Jaula.objects.all()
        for jaula in jaulas:
            jaula = cls.asignarNombreProyecto(jaula) 
        return jaulas

    @classmethod
    def obtenerJaula(cls,id_jaula):
        jaula = cls.find_by_id(id_jaula)
        jaula = cls.asignarNombreProyecto(jaula) 
        return jaula


    @classmethod    
    def asignarNombreProyecto(cls,jaula):
        proyecto = ProyectoService.find_by_id(jaula.id_proyecto)
        jaula.nombre_proyecto= proyecto.nombre
        return jaula

