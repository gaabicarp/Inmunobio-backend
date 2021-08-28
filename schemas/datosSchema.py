from marshmallow import Schema, fields

from .usuarioSchema import UsuariosBase
from .proyectoSchema import ProyectoSchema
from.permisosSchema import PermisoBase
from .espacioFisicoSchema import EspacioFisicoBaseSchema
from .distribuidoraSchema import NuevaDistribuidoraSchema
from .contenedorSchema import ContenedorNuevoSchema
from .herramientaSchema import HerramientaBaseSchema
from .jaulaSchema import JaulaBaseSchema
from .grupoTrabajoSchema import NuevoGrupoDeTrabajoSchema

class DatosSchema(Schema):
    class Meta:
        ordered = True

    proyecto = fields.Nested(ProyectoSchema,many=True)
    espacioFisico= fields.Nested(EspacioFisicoBaseSchema,many=True)
    distribuidora = fields.Nested(NuevaDistribuidoraSchema,many=True)
    contenedor = fields.Nested(ContenedorNuevoSchema,many=True)
    herramienta = fields.Nested(HerramientaBaseSchema,many=True) 
    jaula = fields.Nested(JaulaBaseSchema,many=True)  
    grupoDeTrabajo = fields.Nested(NuevoGrupoDeTrabajoSchema,many=True)  
    
class DatosMysql(Schema):
    class Meta:
        ordered = True
    #Necesario para que al deserializar respete el orden en el que va el json

    permiso = fields.Nested(PermisoBase,many=True) 
    usuario = fields.Nested(UsuariosBase,many=True)

