from flask_restful import Api

from resources.usuariosResource import ActualizarPermisos, Usuarios,UsuariosXIdUsuario,NuevoUsuario, ActualizarPermisos,ObtenerUsuariosParaProyecto
from resources.proyectoResource import *
from resources.permisosResource import Permisos,ObtenerPermisoPorId
from resources.grupoDeTrabajoResource import NuevoGrupoDeTrabajo,ModificarGrupoDeTrabajo,GruposDeTrabajo,RenombrarJefeGrupo
from resources.experimentoResource import ExperimentoResource, Experimentos
from resources.proyectoResource import *
from resources.experimentoResource import ExperimentoResource, Experimentos, CerrarExperimento
from resources.contenedorResource import Contenedor, ContenedorProyecto, ContenedorParent
from resources.stockResource import NuevoStock

api = Api()

api = Api()
#permisos
api.add_resource(ObtenerPermisoPorId, '/api/v1/permisoId')
api.add_resource(Permisos, '/api/v1/permisos')
#usuarios
api.add_resource(ActualizarPermisos, '/api/v1/usuariosPermisos')
api.add_resource(Usuarios, '/api/v1/usuarios')
api.add_resource(UsuariosXIdUsuario, '/api/v1/usuario')
api.add_resource(NuevoUsuario, '/api/v1/nuevoUsuario')
api.add_resource(ObtenerUsuariosParaProyecto, '/api/UsuariosParaProyecto')
#proyectos
api.add_resource(Proyectos, '/api/proyectos')
api.add_resource(NuevoProyecto, '/api/nuevoProyecto')
api.add_resource(ProyectoID, '/api/proyectoID')
api.add_resource(CerrarProyecto, '/api/cerrarProyecto')
api.add_resource(ModificarProyecto, '/api/modificarProyecto')

#Grupo de trabajo
api.add_resource(NuevoGrupoDeTrabajo, '/api/v1/nuevoGrupoDeTrabajo')
api.add_resource(ModificarGrupoDeTrabajo,'/api/v1/modificarGrupo')
api.add_resource(RenombrarJefeGrupo, '/api/v1/nuevoJefeDeGrupo')
api.add_resource(GruposDeTrabajo, '/api/v1/gruposDeTrabajo')
api.add_resource(GrupoDeTrabajo, '/api/v1/grupoDeTrabajo/<int:idGrupoDeTrabajo>')

#stock
api.add_resource(NuevoStock, '/api/v1/NuevoStock')


#experimentos
api.add_resource(Experimentos, '/api/v1/proyecto/<int:idProyecto>/experimentos')
api.add_resource(ExperimentoResource, '/api/v1/experimento/<int:idExperimiento>', endpoint='experimento')
api.add_resource(ExperimentoResource, '/api/v1/nuevoExperimento', endpoint='nuevo_experimento')
api.add_resource(ExperimentoResource, '/api/v1/experimento/gruposExperimentales', endpoint='agregar_grupos_experimentales')
api.add_resource(CerrarExperimento, '/api/v1/cerrarExperimento', endpoint='cerrar_experimento')

#contenedor
api.add_resource(Contenedor, '/api/v1/contenedores', endpoint='contenedores')
api.add_resource(Contenedor, '/api/v1/nuevoContenedor', endpoint='nuevo_contenedore')
api.add_resource(ContenedorProyecto, '/api/v1/contenedoresDelProyecto', endpoint='contenedores_del_proyecto')
api.add_resource(ContenedorProyecto, '/api/v1/asignarProyectoAlContenedor', endpoint='asignar_proyecto_al_contenedor')
api.add_resource(ContenedorParent, '/api/v1/subcontenedores', endpoint='subcontenedores')
api.add_resource(ContenedorParent, '/api/v1/asignarParentAContenedores', endpoint='asignar_parent_a_contenedores')