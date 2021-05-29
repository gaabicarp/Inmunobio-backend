from dateutil import parser
import datetime
from flask import jsonify
from models.mysql.usuario import Usuario
from models.mongo.proyecto import Proyecto, ProyectoSchema, ProyectoCerradoSchema, ProyectoModificarSchema,ProyectoNuevoSchema
from servicios.usuarioService import UsuarioService
class ProyectoService:
    @classmethod
    def find_all(cls):
        return jsonify(ProyectoSchema().dump(Proyecto.objects.filter(finalizado=False).all(), many=True))
        
    @classmethod
    def find_by_id(cls, id):
        return Proyecto.objects.filter(id_proyecto=id).first()

    @classmethod
    def nuevoProyecto(cls, datos):
        proyecto = ProyectoNuevoSchema().load(datos)
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
    
    @classmethod
    def modificarProyecto(cls, datos):
        proyecto = ProyectoModificarSchema().load(datos)
        if proyecto.descripcion.strip() != "":
            Proyecto.objects(id_proyecto = proyecto.id_proyecto).update(set__descripcion = proyecto.descripcion)
        Proyecto.objects(id_proyecto = proyecto.id_proyecto).update(set__montoInicial = proyecto.montoInicial)
    
    @classmethod
    def agregarMiembros(self):
        usuariosIdPermitidas = UsuarioService.UsuarioService()
        return usuariosIdPermitidas