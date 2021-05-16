from flask_restful import Api

from resources.usuariosResource import ActualizarPermisos, Usuarios,UsuariosXIdUsuario,NuevoUsuario, ActualizarPermisos,ObtenerUsuariosParaProyecto
from resources.proyectoResource import *
from resources.permisosResource import Permisos,ObtenerPermisoPorId
from resources.grupoDeTrabajoResource import NuevoGrupoDeTrabajo,GrupoDeTrabajo,GruposDeTrabajo,RenombrarJefeGrupo
from resources.experimentoResource import ExperimentoResource, Experimentos

from resources.proyectoResource import *
from resources.experimentoResource import ExperimentoResource, Experimentos, CerrarExperimento
from resources.contenedorResource import Contenedor, ContenedorProyecto, ContenedorParent
from resources.grupoExperimentalResource import GrupoExperimental, GruposExperimentales
from resources.jaulaResource import Jaula, JaulasSinProyecto, JaulasDelProyecto
from resources.fuenteExperimentalResource import FuenteExperimental
from resources.animalResource import  Animal, Animales, AnimalesSinJaula, AnimalesDeLaJaula

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
api.add_resource(Proyectos, '/api/v1/proyectos')
api.add_resource(NuevoProyecto, '/api/v1/nuevoProyecto')
api.add_resource(ProyectoID, '/api/proyectoID')
api.add_resource(CerrarProyecto, '/api/cerrarProyecto')
api.add_resource(ModificarProyecto, '/api/modificarProyecto')

#Grupo de trabajo
api.add_resource(NuevoGrupoDeTrabajo, '/api/v1/nuevoGrupoDeTrabajo')
api.add_resource(GrupoDeTrabajo, '/api/v1/GrupoDeTrabajo')
api.add_resource(GruposDeTrabajo, '/api/v1/GruposDeTrabajo')
api.add_resource(RenombrarJefeGrupo, '/api/v1/NuevoJefeDeGrupo')

#Experimento
api.add_resource(Experimentos, '/api/v1/proyecto/<int:idProyecto>/experimentos', endpoint='experimentos')
api.add_resource(ExperimentoResource, '/api/v1/experimento/<int:idExperimiento>', endpoint='experimento')
api.add_resource(ExperimentoResource, '/api/v1/nuevoExperimento', endpoint='nuevo_experimento')
api.add_resource(CerrarExperimento, '/api/v1/cerrarExperimento', endpoint='cerrar_experimento')
api.add_resource(ExperimentoResource, '/api/v1/modificarExperimento', endpoint='modificar_experimento')

#Grupo Experimental
api.add_resource(GrupoExperimental, '/api/v1/grupoExperimental/<int:idGrupoExperimental>', endpoint='grupo_experimental')
api.add_resource(GrupoExperimental, '/api/v1/nuevoGrupoExperimental', endpoint='nuevo_grupo_experimental')
api.add_resource(GruposExperimentales, '/api/v1/experimento/<int:idExperimento>/gruposExperimentales', endpoint='grupos_experimentales_del_experimento')

#Jaula
api.add_resource(Jaula, '/api/v1/jaula/<int:idJaula>', endpoint="jaula_por_id")
api.add_resource(Jaula, '/api/v1/asignarJaulaAProyecto', endpoint="asignar_jaula_a_proyecto")
api.add_resource(Jaula, '/api/v1/nuevaJaula', endpoint="nueva_jaula")
api.add_resource(Jaula, '/api/v1/bajarJaula/<int:idJaula>', endpoint="bajar_jaula")
api.add_resource(JaulasSinProyecto, '/api/v1/jaulasDisponibles', endpoint="jaulas_disponibles")
api.add_resource(JaulasDelProyecto, '/api/v1/proyecto/<int:idProyecto>/jaulasDelProyecto', endpoint="jaulas_del_proyecto")

#FuenteExperimental
api.add_resource(FuenteExperimental, '/api/v1/fuenteExperimental/<int:idFuenteExperimental>', endpoint="fuente_experimental")

#Animal
api.add_resource(Animal, '/api/v1/animal/<int:idAnimal>', endpoint="animal")
api.add_resource(Animal, '/api/v1/bajaAnimal/<int:idAnimal>', endpoint="baja_animal")
api.add_resource(Animal, '/api/v1/nuevoAnimal', endpoint="nuevo_animal")
api.add_resource(Animales, '/api/v1/animales', endpoint="animales")
api.add_resource(AnimalesSinJaula, '/api/v1/animalesSinJaula', endpoint="animales_sin_jaula")
api.add_resource(AnimalesDeLaJaula, '/api/v1/jaula/<int:idJaula>/animales', endpoint="animales_de_la_jaula")
api.add_resource(AnimalesDeLaJaula, '/api/v1/asignarJaulas', endpoint="asignar_jaulas")

api.add_resource(Contenedor, '/api/v1/contenedores', endpoint='contenedores')
api.add_resource(Contenedor, '/api/v1/nuevoContenedor', endpoint='nuevo_contenedore')
api.add_resource(ContenedorProyecto, '/api/v1/contenedoresDelProyecto', endpoint='contenedores_del_proyecto')
api.add_resource(ContenedorProyecto, '/api/v1/asignarProyectoAlContenedor', endpoint='asignar_proyecto_al_contenedor')
api.add_resource(ContenedorParent, '/api/v1/subcontenedores', endpoint='subcontenedores')
api.add_resource(ContenedorParent, '/api/v1/asignarParentAContenedores', endpoint='asignar_parent_a_contenedores')