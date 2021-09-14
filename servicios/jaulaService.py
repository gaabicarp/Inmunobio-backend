from servicios.validationService import Validacion
from models.mongo.jaula import Jaula
from schemas.jaulaSchema import BusquedaBlogsJaula,JaulaSchema,BusquedaBlogJaula,NuevaJaulaSchema, ActualizarProyectoJaulaSchema, ActualizarJaulaSchema,NuevoBlogJaulaSchema
from servicios.animalService import AnimalService
from servicios.commonService import CommonService

class JaulaService:
    @classmethod
    def find_by_id(cls, idJaula):
        jaula =  Jaula.objects(id_jaula = idJaula).first()
        if not jaula: raise Exception(f"No se encontró ninguna jaula con el id {idJaula}")
        return jaula

    @classmethod
    def jaulasSinAsignar(cls):
        return Jaula.objects(id_proyecto = 0).all()
    
    @classmethod
    def jaulasDelProyecto(cls, idProyecto):
        return Jaula.objects(id_proyecto = idProyecto)

    @classmethod
    def jaulaPerteneceAlProyecto(cls,_id_proyecto,_id_jaula):
        cls.find_by_id(_id_jaula)
        if not cls.jaulasDelProyecto(_id_proyecto).filter(id_jaula = _id_jaula).first(): raise Exception( f"La jaula {_id_jaula} no se encuentra asignada al proyecto con id {_id_proyecto}")

    @classmethod
    def crearJaula(cls, datos):
        #aca nunca validar si existe el proyecto ->no porque siempre se asigna aparte
        jaula = NuevaJaulaSchema().load(datos)
        #cls.verificarProyecto(jaula.id_proyecto)
        jaula.save()
    
    def verificarProyecto(idProyecto):
        if not Validacion().elProyectoExiste(idProyecto):
            raise Exception(f"El proyecto con id {idProyecto} no existe.")
        if not Validacion().elProyectoEstaActivo(idProyecto):
            raise Exception(f"El proyecto con id {idProyecto} no se encuentra activo")

    @classmethod
    def actualizarProyectoDeLaJaula(cls, datos):
        jaula = ActualizarProyectoJaulaSchema().load(datos)
        cls.validaModificacionJaula(jaula)
        Jaula.objects(id_jaula = jaula.id_jaula).update(
            set__id_proyecto = jaula.id_proyecto
        )
        AnimalService.actualizarProyectoAnimalesDeJaulas(jaula)
        
    @classmethod
    def validaModificacionJaula(cls,jaula):
        cls.find_by_id(jaula.id_jaula)
        cls.verificarProyecto(jaula.id_proyecto)

    @classmethod
    def actualizarJaula(cls, datos):
        ActualizarJaulaSchema().dump(datos)
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
        if len(AnimalService.animalesDeLaJaula(idJaula)) > 0 : raise Exception("La jaula contiene animales activos, no puede darse de baja.")

    @classmethod
    def nuevoBlogJaula(cls, datos):
        NuevoBlogJaulaSchema().load(datos)
        cls.crearBlogJaula(datos['id_jaula'],datos['blogs'])

    @classmethod
    def crearBlogJaula(cls,id_jaula,datosBlog):
        from servicios.blogService import BlogService
        jaula = cls.find_by_id(id_jaula)
        jaula.blogs.append(BlogService.nuevoBlog(datosBlog))
        jaula.save()

    @classmethod
    def borrarBlogJaula(cls,_id_jaula,_id_blog):
        cls.validarBlogJaula(_id_jaula,_id_blog)
        Jaula.objects.filter(id_jaula = _id_jaula).first().modify(pull__blogs__id_blog =_id_blog)
            
    @classmethod
    def validarBlogJaula(cls,_id_jaula,_id_blog):
        cls.find_by_id(_id_jaula)
        cls.validarExistenciaBlog(_id_jaula,_id_blog)

    @classmethod
    def validarExistenciaBlog(_id_jaula,_id_blog):
        if not Jaula.objects.filter(id_jaula = _id_jaula, blogs__id_blog= _id_blog).first() : raise Exception(f"No se encontró ningun blog con el id: {_id_blog}") 

    @classmethod
    def blogsDeTodasLasJaulas(cls,datos):
        BusquedaBlogsJaula().load(datos)
        return cls.obtenerTodosLosBlogs(cls.obtenerJaulas(),datos)

    @classmethod
    def obtenerTodosLosBlogs(cls,jaulas,datos):
        return [x for x in list(map(lambda jaula: cls.obtenerBlogs(jaula,datos),jaulas)) if x ]

    @classmethod
    def obtenerBlogsDeJaula(cls,datos):
        BusquedaBlogJaula().load(datos)
        jaula = cls.find_by_id(datos['id_jaula'])
        return cls.obtenerBlogs(jaula,datos)

    @classmethod
    def obtenerBlogs(cls,jaula,datos):
        from servicios.blogService import BlogService
        blogs = BlogService.busquedaPorFecha(jaula.blogs,datos['fechaDesde'],datos['fechaHasta'])
        return cls.deserializarBlogsJaulas(blogs,jaula) 

    @classmethod
    def deserializarBlogsJaulas(cls,blogs,jaula):
        return list(map(lambda blog: cls.agregarDatosExtraBlogJaula(blog,jaula),blogs))
    
    @classmethod
    def agregarDatosExtraBlogJaula(cls,blog,jaula):
        from schemas.blogSchema import BlogSchemaExtendido
        dictBlog =  BlogSchemaExtendido().dump(blog)
        dictBlog['id_jaula'] = jaula.id_jaula
        dictBlog['codigoJaula'] = jaula.codigo
        return dictBlog

    @classmethod
    def obtenerBlogsJaulaDeProyecto(cls,_id_proyecto,datos):
        jaulas = cls.jaulasDelProyecto(_id_proyecto)
        return cls.obtenerTodosLosBlogs(jaulas,datos)

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
