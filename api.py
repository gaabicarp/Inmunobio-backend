from flask_restful import Api
from resources.usuarios import Usuarios,UsuarioxUsername,UsuariosXIdUsuario,NuevoUsuario, ActualizarPermisos,ObtenerUsuariosParaProyecto
from resources.proyectoResource import *
from resources.experimentoResource import ExperimentoResource, Experimentos, CerrarExperimento
from resources.contenedorResource import Contenedor, ContenedorProyecto, ContenedorParent
from resources.grupoDeTrabajo import NuevoGrupoDeTrabajo,GrupoDeTrabajo,GruposDeTrabajo

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



api.add_resource(Experimentos, '/api/v1/proyecto/<int:idProyecto>/experimentos')
api.add_resource(ExperimentoResource, '/api/v1/experimento/<int:idExperimiento>', endpoint='experimento')
api.add_resource(ExperimentoResource, '/api/v1/nuevoExperimento', endpoint='nuevo_experimento')
api.add_resource(ExperimentoResource, '/api/v1/experimento/gruposExperimentales', endpoint='agregar_grupos_experimentales')
api.add_resource(CerrarExperimento, '/api/v1/cerrarExperimento', endpoint='cerrar_experimento')

api.add_resource(Contenedor, '/api/v1/contenedores', endpoint='contenedores')
api.add_resource(Contenedor, '/api/v1/nuevoContenedor', endpoint='nuevo_contenedore')
api.add_resource(ContenedorProyecto, '/api/v1/contenedoresDelProyecto', endpoint='contenedores_del_proyecto')
api.add_resource(ContenedorProyecto, '/api/v1/asignarProyectoAlContenedor', endpoint='asignar_proyecto_al_contenedor')
api.add_resource(ContenedorParent, '/api/v1/subcontenedores', endpoint='subcontenedores')
api.add_resource(ContenedorParent, '/api/v1/asignarParentAContenedores', endpoint='asignar_parent_a_contenedores')