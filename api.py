from flask_restful import Api
from resources.usuarios import Usuarios,UsuarioxUsername,UsuariosXIdUsuario,NuevoUsuario, ActualizarPermisos,ObtenerUsuariosParaProyecto
from resources.proyecto import *

from resources.grupoDeTrabajo import NuevoGrupoDeTrabajo,GrupoDeTrabajo,GruposDeTrabajo

from resources.experimento import ExperimentoResource, Experimentos
api = Api()

api.add_resource(Usuarios, '/api/usuarios')
api.add_resource(UsuarioxUsername, '/api/usuario/<string:username>')
api.add_resource(UsuariosXIdUsuario, '/api/usuario/<int:id>')
api.add_resource(NuevoUsuario, '/api/nuevoUsuario')
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

