from models.mongo.experimento import Experimento
from schemas.experimentoSchema import BusquedaBlogExp,NuevoBlogExpSchema, ExperimentoSchema, ModificarExperimentoSchema, AltaExperimentoSchema, CerrarExperimentoSchema, AgregarMuestrasAlExperimentoSchema
from .validationService import Validacion
from models.mongo.experimento import Experimento 
from servicios.muestraService import MuestraService
from servicios.blogService import BlogService
from dateutil import parser
import datetime
from exceptions.exception import ErrorExperimentoInexistente,ErrorExpDeProyecto

class ExperimentoService:    
    @classmethod
    def find_by_id(cls, idExperimento):
        exp =  Experimento.objects.filter(id_experimento=idExperimento).first()
        if not exp : raise ErrorExperimentoInexistente(idExperimento)
        return exp

    @classmethod
    def find_all_by_idProyecto(cls, idProyecto):
        return ExperimentoSchema().dump(Experimento.objects.filter(id_proyecto=idProyecto).all(), many=True)
    @classmethod
    def find_all_by_id(cls, idProyecto):
        return Experimento.objects.filter(id_proyecto=idProyecto).all()
    
    @classmethod
    def nuevoExperimento(cls, datos):
        #falta validar q exista el proyecto
        experimento = AltaExperimentoSchema().load(datos)
        experimento.save()
    
    @classmethod
    def cerrarExperimento(cls, datos):
        experimento = CerrarExperimentoSchema().load(datos)
        Experimento.objects(id_experimento=experimento.id_experimento).update(
            fechaFin = parser.parse(str(datetime.datetime.utcnow())),
            resultados = experimento.resultados,
            finalizado = True,
            conclusiones = experimento.conclusiones
        )
    
    @classmethod
    def modificarExperimento(cls, datos):
        experimento = ModificarExperimentoSchema().load(datos)
        Experimento.objects(id_experimento=experimento.id_experimento).update(
            resultados= experimento.resultados,
            metodologia = experimento.metodologia,
            objetivos = experimento.objetivos,
            muestrasExternas = experimento.muestrasExternas
        )

    def lasMuestrasSonDelMismoProyectoDelExperimento(self, experimento):
        return all(experimento.id_proyecto == muestraExterna.id_proyecto for muestraExterna in experimento.muestrasExternas)
        
    def lasMuestrasEstanHabilitadas(self, experimento):
        return all(MuestraService.validarMuestra(muestra.id_muestra) for muestra in experimento.muestrasExternas)

    def validarMuestrasExternas(self, experimento):
        if not self.lasMuestrasSonDelMismoProyectoDelExperimento(self, experimento):
            raise ValueError("Todas las muestras tienen que ser del mismo proyecto.")
        if self.lasMuestrasEstanHabilitadas(self, experimento):
            raise ValueError("Todas las muestras tienen que estar habilitadas.")

    @classmethod
    def agregarMuestrasExternasAlExperimento(cls, datos):
        AgregarMuestrasAlExperimentoSchema().load(datos)
        experimento = AgregarMuestrasAlExperimentoSchema().load(datos)
        cls.validarMuestrasExternas(cls, experimento)
        Experimento.objects(id_experimento = experimento.id_experimento).update(muestrasExternas=experimento.muestrasExternas)

    def nuevoBlogExperimento(cls, datos):
        NuevoBlogExpSchema().load(datos)
        cls.crearBlogExp(cls,datos['id_experimento'],datos['blogs'])

    @classmethod
    def crearBlogExp(cls,id_experimento,datosBlog):
        from servicios.blogService import BlogService
        experimento = cls.find_by_id(id_experimento)
        blog = BlogService.nuevoBlog(datosBlog)
        experimento.blogs.append(blog)
        experimento.save()

    @classmethod
    def expPerteneceAlProyecto(cls,id_proyecto,id_experimento):
        exp = cls.find_by_id(id_experimento)
        if not exp.id_proyecto == id_proyecto: raise ErrorExpDeProyecto(id_proyecto,id_experimento)

    @classmethod
    def obtenerBlogs(cls,datos):
        BusquedaBlogExp().load(datos)
        experimento = cls.find_by_id(datos['id_experimento'])
        blogs= BlogService.busquedaPorFecha(experimento.blogs,datos['fechaDesde'],datos['fechaHasta'])
        return cls.deserializarBlogsExp(blogs,experimento)

    def removerMuestraDeExperimento(cls, idExperimento, idMuestra):
        cls.validarRemoverMuestraExperimento(idExperimento, idMuestra)
        Experimento.objects(id_experimento=idExperimento).update(pull__muestrasExternas__id_muestra=idMuestra)
    
    def validarRemoverMuestraExperimento(idExperimento, idMuestra):
        if not Validacion().elExperimentoExiste(idExperimento):
            raise Exception(f"El experimento con id {idExperimento} no existe.")
        if not Validacion().existeLaMuestra(idMuestra):
            raise Exception(f"La muestra con id {idMuestra} no existe.")
        if not Validacion().elExperimentoTieneLaMuestra(idExperimento, idMuestra):
            raise Exception(f"El experimento con id {idExperimento} no tiene la muestra con id {idMuestra}.")

    @classmethod
    def obtenerBlogsExperimento(cls,_id_proyecto,datos):
        experimentos = cls.find_all_by_id(_id_proyecto)
        return cls.obtenerLosBlogs(experimentos,datos)

        #BlogSchema().dump(many=True))
    @classmethod
    def blogServiceExp(cls,blogs,fechaDesde,fechaHasta):
        from servicios.blogService import BlogService
        return BlogService.busquedaPorFecha(blogs,fechaDesde,fechaHasta)

    @classmethod
    def obtenerLosBlogs(cls,experimentos,datos):
        blogs = []
        for exp in experimentos:
            blogsExperimentos= cls.blogServiceExp(exp.blogs,datos['fechaDesde'],datos['fechaHasta'])
            blogs.extend(cls.deserializarBlogsExp(blogsExperimentos,exp))
        return blogs

    @classmethod
    def deserializarBlogsExp(cls,blogs,exp):
        blogsDic = []
        for blog in blogs: blogsDic.append(cls.agregarDatosExtraBlogExp(blog,exp))
        return blogsDic

    @classmethod
    def agregarDatosExtraBlogExp(cls,blog,exp):
        from schemas.blogSchema import BlogSchema
        dictBlog =  BlogSchema().dump(blog)
        dictBlog['codigoExperimento'] = exp.codigo
        return dictBlog
