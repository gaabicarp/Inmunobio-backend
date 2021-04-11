from flask_restful import Api
from resources.usuarios import Usuarios,UsuarioxUsername,UsuariosXIdUsuario,NuevoUsuario, ActualizarPermisos,ObtenerUsuariosParaProyecto
from resources.proyecto import *
<<<<<<< HEAD
from resources.grupoDeTrabajo import NuevoGrupoDeTrabajo,GrupoDeTrabajoPorId
=======
from resources.experimento import ExperimentoResource, Experimentos
>>>>>>> 0d696975cbdbdf5e3394b276649effc6be63d9b5
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
api.add_resource(GrupoDeTrabajoPorId, '/api/GrupoDeTrabajoPorId/<int:id>')


api.add_resource(Experimentos, '/api/proyecto/<int:idProyecto>/experimentos')
api.add_resource(ExperimentoResource, '/api/experimento/<int:idExperimiento>', endpoint='experimento')
api.add_resource(ExperimentoResource, '/api/nuevoExperimento', endpoint='nuevo_experimento')
api.add_resource(ExperimentoResource, '/api/cerrarExperimento/<int:idExperimento>', endpoint='cerrar_experimento')

