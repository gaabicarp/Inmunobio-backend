from flask_restful import Api
from resources.usuarios import Usuarios,UsuarioxUsername,UsuariosXIdUsuario,NuevoUsuario, ActualizarPermisos,ObtenerUsuariosParaProyecto
from resources.proyectoResource import *
from resources.grupoDeTrabajo import NuevoGrupoDeTrabajo,GrupoDeTrabajoPorId
from resources.experimentoResource import ExperimentoResource, Experimentos, CerrarExperimento
api = Api()

api.add_resource(Usuarios, '/api/usuarios')
api.add_resource(UsuarioxUsername, '/api/usuario/<string:username>')
api.add_resource(UsuariosXIdUsuario, '/api/usuario/<int:id>')
api.add_resource(NuevoUsuario, '/api/nuevoUsuario')
api.add_resource(ObtenerUsuariosParaProyecto, '/api/UsuariosParaProyecto')

api.add_resource(Proyectos, '/api/v1/proyectos')
api.add_resource(NuevoProyecto, '/api/v1/nuevoProyecto')
api.add_resource(ProyectoID, '/api/v1/proyectoID')
api.add_resource(CerrarProyecto, '/api/v1/cerrarProyecto')
api.add_resource(ModificarProyecto, '/api/v1/modificarProyecto')
#Grupo de trabajo
api.add_resource(NuevoGrupoDeTrabajo, '/api/nuevoGrupoDeTrabajo')
api.add_resource(GrupoDeTrabajoPorId, '/api/GrupoDeTrabajoPorId/<int:id>')


api.add_resource(Experimentos, '/api/v1/proyecto/<int:idProyecto>/experimentos')
api.add_resource(ExperimentoResource, '/api/v1/experimento/<int:idExperimiento>', endpoint='experimento')
api.add_resource(ExperimentoResource, '/api/v1/nuevoExperimento', endpoint='nuevo_experimento')
api.add_resource(ExperimentoResource, '/api/v1/experimento/gruposExperimentales', endpoint='agregar_grupos_experimentales')
api.add_resource(CerrarExperimento, '/api/v1/cerrarExperimento', endpoint='cerrar_experimento')

