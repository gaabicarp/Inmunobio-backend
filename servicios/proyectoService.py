from dateutil import parser
import datetime
from flask import jsonify
from models.mongo.proyecto import Proyecto, ProyectoSchema, ProyectoCerradoSchema, ProyectoModificarSchema,ProyectoNuevoSchema
from servicios.usuarioService import UsuarioService
from servicios.commonService import CommonService
from schemas.usuarioSchema import UsuarioSchema
from exceptions.exception import ErrorUsuarioInexistente

class ProyectoService:
    @classmethod
    def find_all(cls):
        return jsonify(ProyectoSchema().dump(Proyecto.objects.filter().all(), many=True))
        
    @classmethod
    def find_by_id(cls, id):
        return Proyecto.objects.filter(id_proyecto=id).first()

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
        try:
            proyecto = cls.find_by_id(id_proyecto)
            usuarios = UsuarioService.busquedaUsuariosID(proyecto.participantes)
            return CommonService.jsonMany(usuarios,UsuarioSchema)
        except ErrorUsuarioInexistente as err:
            return {'Error': err.message},400  


    @classmethod
    def json(cls,datos):
        return  ProyectoSchema().dump(datos)

