from models.mongo.jaula import Jaula
from exceptions.exception import ErrorEspacioFisicoInexistente,ErrorJaulaInexistente,ErrorBlogInexistente,ErrorJaulaDeProyecto,ErrorJaulaBaja,ErrorEspacioDeproyecto
from schemas.jaulaSchema import  JaulaSchemaBlogs,BusquedaBlogsJaula,JaulaSchema,BlogSchema,BusquedaBlogJaula,NuevaJaulaSchema, ActualizarProyectoJaulaSchema, ActualizarJaulaSchema,NuevoBlogJaulaSchema
from servicios.animalService import AnimalService
from servicios.commonService import CommonService

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
    def jaulaPerteneceAlProyecto(cls,_id_proyecto,_id_jaula):
        if not cls.jaulasDelProyecto(_id_proyecto).filter(id_jaula = _id_jaula):
            raise ErrorJaulaDeProyecto(_id_proyecto,_id_jaula)

    @classmethod
    def crearJaula(cls, datos):
        #aca nunca validar si existe el proyecto, se asigna aparte
        jaula = NuevaJaulaSchema().load(datos)
        jaula.save()

    @classmethod
    def actualizarProyectoDeLaJaula(cls, datos):
        from servicios.proyectoService import ProyectoService
        jaula = ActualizarProyectoJaulaSchema().load(datos)
        ProyectoService.find_by_id(jaula.id_proyecto)
        Jaula.objects(id_jaula = jaula.id_jaula).update(
            id_proyecto = jaula.id_proyecto
        )

    @classmethod
    def actualizarJaula(cls, datos):
        jaulaAct = ActualizarJaulaSchema().dump(datos)
        jaula = cls.find_by_id(datos['id_jaula'])
        CommonService.updateAtributes(jaula,datos)
        jaula.save()

    @classmethod
    def bajarJaula(cls, idJaula):
        jaula = cls.find_by_id(idJaula)
        cls.laJaulaTieneAnimales(idJaula)
        jaula.delete()
        return {'Status':'Ok'}, 200
    @classmethod
    def laJaulaTieneAnimales(cls, idJaula):
        animales = AnimalService.animalesDeLaJaula(idJaula)
        if len(animales) > 0 : raise ErrorJaulaBaja

    @classmethod
    def nuevoBlogJaula(cls, datos):
        NuevoBlogJaulaSchema().load(datos)
        cls.crearBlogJaula(datos['id_jaula'],datos['blogs'])

    @classmethod
    def crearBlogJaula(cls,id_jaula,datosBlog):
        from servicios.blogService import BlogService
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
        return cls.blogServiceJaulas(jaula.blogs,datos['fechaDesde'],datos['fechaHasta'])

    @classmethod
    def blogServiceJaulas(cls,blogs,fechaDesde,fechaHasta):
        from servicios.blogService import BlogService
        return BlogService.busquedaPorFecha(blogs,fechaDesde,fechaHasta)

    @classmethod
    def obtenerTodosLosBlogs(cls,datos):
        BusquedaBlogsJaula().load(datos)
        blogs = []
        jaulas = cls.obtenerJaulas()
        for jaula in jaulas:
            blogsJaula= cls.blogServiceJaulas(jaula.blogs,datos['fechaDesde'],datos['fechaHasta'])
            blogs.extend(cls.deserializarBlogsJaulas(blogsJaula,jaula))
        return blogs

    @classmethod
    def deserializarBlogsJaulas(cls,blogs,jaula):
        blogsDic = []
        for blog in blogs: blogsDic.append(cls.agregarDatosExtraBlogJaula(blog,jaula))
        return blogsDic

    @classmethod
    def agregarDatosExtraBlogJaula(cls,blog,jaula):
        dictBlog =  BlogSchema().dump(blog)
        dictBlog['id_jaula'] = jaula.id_jaula
        dictBlog['codigoJaula'] = jaula.codigo
        return dictBlog

    @classmethod
    def obtenerJaulas(cls):
        return  Jaula.objects.all()

    @classmethod
    def obtenerTodasLasJaulas(cls):
        jaulas = JaulaSchema().dump(cls.obtenerJaulas(),many=True)
        cls.asignarDatosExtra(jaulas)
        return jaulas

    @classmethod
    def asignarDatosExtra(cls,jaulas):
        for jaula in jaulas: cls.asignarProyectoYEspFisico(jaula)

    @classmethod
    def asignarProyectoYEspFisico(cls,jaula):
        return CommonService.asignarNombreProyecto(CommonService.asignarNombreEspacioFisico(jaula))
    
    @classmethod
    def obtenerJaula(cls,id_jaula):
        return cls.asignarProyectoYEspFisico(JaulaSchema().dump(cls.find_by_id(id_jaula))) 
