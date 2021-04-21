from flask_restful import Api
from resources.usuariosResource import ActualizarPermisos, Usuarios,UsuariosXIdUsuario,NuevoUsuario, ActualizarPermisos,ObtenerUsuariosParaProyecto
from resources.proyecto import *
from resources.permisosResource import Permisos,ObtenerPermisoPorId
from resources.grupoDeTrabajo import NuevoGrupoDeTrabajo,GrupoDeTrabajo,GruposDeTrabajo
from resources.experimento import ExperimentoResource, Experimentos

api = Api()
#permisos
api.add_resource(ObtenerPermisoPorId, '/api/v1/permisoId')
api.add_resource(Permisos, '/api/v1/permisos')

api.add_resource(ActualizarPermisos, '/api/v1/usuariosPermisos')
api.add_resource(Usuarios, '/api/v1/usuarios')
api.add_resource(UsuariosXIdUsuario, '/api/v1/usuario')
api.add_resource(NuevoUsuario, '/api/v1/nuevoUsuario')
api.add_resource(ObtenerUsuariosParaProyecto, '/api/UsuariosParaProyecto')

api.add_resource(Proyectos, '/api/proyectos')
api.add_resource(NuevoProyecto, '/api/nuevoProyecto')
api.add_resource(ProyectoID, '/api/proyectoID')
api.add_resource(CerrarProyecto, '/api/cerrarProyecto')
api.add_resource(ModificarProyecto, '/api/modificarProyecto')

#Grupo de trabajo
api.add_resource(NuevoGrupoDeTrabajo, '/api/nuevoGrupoDeTrabajo')
api.add_resource(GrupoDeTrabajo, '/api/GrupoDeTrabajo/<int:id>')
api.add_resource(GruposDeTrabajo, '/api/GruposDeTrabajo')



api.add_resource(Experimentos, '/api/proyecto/<int:idProyecto>/experimentos')
api.add_resource(ExperimentoResource, '/api/experimento/<int:idExperimiento>', endpoint='experimento')
api.add_resource(ExperimentoResource, '/api/nuevoExperimento', endpoint='nuevo_experimento')
api.add_resource(ExperimentoResource, '/api/cerrarExperimento/<int:idExperimento>', endpoint='cerrar_experimento')

