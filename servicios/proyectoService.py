from dateutil import parser
import datetime
from models.mongo.proyecto import Proyecto
from schemas.proyectoSchema import ProyectoExtendido,NuevoBlogProyectoSchema,ObtenerBlogsProyectoSchema, ProyectoCerradoSchema, ProyectoModificarSchema,ProyectoNuevoSchema
from exceptions.exception import ErrorProyectoInexistente
from servicios.commonService import CommonService

class ProyectoService:
    @classmethod
    def find_all(cls):
        proyectos =  Proyecto.objects.filter().all()
        [cls.agregarDatosProyecto(proyecto) for proyecto in proyectos]
        return proyectos
    @classmethod
    def find_by_id(cls, id):
        proyecto =  Proyecto.objects.filter(id_proyecto=id).first()
        if not proyecto: raise ErrorProyectoInexistente(id)
        return proyecto

    @classmethod
    def nuevoProyecto(cls, datos):
        proyecto = ProyectoNuevoSchema().load(datos)
        cls.validarProyecto(proyecto)
        proyecto.save()

    @classmethod
    def validarProyecto(cls,proyecto):
        from servicios.usuarioService import UsuarioService
        UsuarioService.busquedaUsuariosID(proyecto.participantes)
        from servicios.permisosService import PermisosService
        PermisosService.esJefeDeProyecto(UsuarioService.find_by_id(proyecto.idDirectorProyecto))

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
        cls.validarProyecto(proyecto)
        if proyecto.descripcion.strip() != "":
            Proyecto.objects(id_proyecto = proyecto.id_proyecto).update(set__descripcion = proyecto.descripcion)
        Proyecto.objects(id_proyecto = proyecto.id_proyecto).update(set__montoInicial = proyecto.montoInicial,set__participantes = proyecto.participantes)

    @classmethod
    def obtenerMiembrosProyecto(cls, id_proyecto):  
        from servicios.usuarioService import UsuarioService
        proyecto = cls.find_by_id(id_proyecto)
        return UsuarioService.busquedaUsuariosID(proyecto.participantes)

    @classmethod
    def obtenerBlogsProyecto(cls,datos):
        ObtenerBlogsProyectoSchema().load(datos)
        proyecto = cls.find_by_id(datos['id_proyecto'])
        return cls.blogsProyecto(proyecto.id_proyecto,datos)

    @classmethod
    def blogsProyecto(cls,id_proyecto,datos):
        from servicios.jaulaService import JaulaService
        blogsJaula = JaulaService.obtenerBlogsJaulaDeProyecto(id_proyecto,datos)

        from servicios.experimentoService import ExperimentoService
        blogsExperimento = ExperimentoService.obtenerBlogsExperimento(id_proyecto,datos)

        return blogsJaula+blogsExperimento    

    @classmethod
    def nuevoBlogsProyecto(cls,datos):
        NuevoBlogProyectoSchema().load(datos)
        if cls.esBlogJaula(datos['blogs']): cls.crearBlogProyectoJaula(datos)
        else: cls.crearBlogProyectoExperimento(datos)

    @classmethod
    def crearBlogProyectoExperimento(cls,datos):
        from servicios.experimentoService import ExperimentoService
        ExperimentoService.crearBlogExp(datos['id'],datos['blogs'])

    @classmethod
    def crearBlogProyectoJaula(cls,datos):
        from servicios.jaulaService import JaulaService
        cls.validarBlogJaulaDeProyecto(datos)
        JaulaService.crearBlogJaula(datos['id'],datos['blogs'])

    @classmethod
    def validarBlogJaulaDeProyecto(cls,datos):
        from servicios.jaulaService import JaulaService
        JaulaService.jaulaPerteneceAlProyecto(datos['id_proyecto'],datos['id'])

    @classmethod
    def validarExpDeProyecto(cls,datos):
        from servicios.experimentoService import ExperimentoService
        ExperimentoService.expPerteneceAlProyecto(datos['id_proyecto'],datos['id'])

    @classmethod
    def esBlogJaula(cls,blog):
        return blog['tipo'] == "Jaula"

    @classmethod
    def obtenerNombreProyecto(cls,id):
        return cls.find_by_id(id).nombre

    @classmethod
    def obtenerProyectosUsuario(cls,id_usuario):
        proyectos =  Proyecto.objects.filter(idDirectorProyecto=id_usuario,participantes=id_usuario)
        [cls.agregarDatosProyecto(proyecto) for proyecto in proyectos]
        return proyectos

    @classmethod
    def obtenerProyecto(cls,id_proyecto):
        proyecto = cls.find_by_id(id_proyecto)
        proyecto.participantes = cls.obtenerMiembrosProyecto(id_proyecto)
        from servicios.usuarioService import UsuarioService
        proyecto.idDirectorProyecto = UsuarioService.find_by_id(proyecto.idDirectorProyecto)
        return proyecto
    
    @classmethod
    def agregarDatosProyecto(cls,proyecto):
        proyecto.participantes = cls.obtenerMiembrosProyecto(proyecto.id_proyecto)
        from servicios.usuarioService import UsuarioService
        proyecto.idDirectorProyecto = UsuarioService.find_by_id(proyecto.idDirectorProyecto)
