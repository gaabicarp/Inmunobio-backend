from flask_restful import Api

from resources.usuariosResource import  ObtenerUsuariosResource,UsuarioResource, UsuarioID,ObtenerUsuariosParaProyecto
from resources.proyectoResource import *
from resources.permisosResource import Permisos,ObtenerPermisoPorId
from resources.grupoDeTrabajoResource import GrupoDeTrabajoID,GrupoDeTrabajo,GruposDeTrabajo,RenombrarJefeGrupo
from resources.experimentoResource import ExperimentoResource, Experimentos
from resources.proyectoResource import *
from resources.experimentoResource import ExperimentoResource, Experimentos, CerrarExperimento
from resources.contenedorResource import Contenedor, ContenedorProyecto, ContenedorParent

from resources.stockResource import ObtenerProductosStock,ProductoEnStock,BorrarTodoStock,ConsumirStockResource,ProductoEnStockID
from resources.productoResource import ProductoResource,ObtenerProductosResource,ProductoID,ArchivoProducto
from resources.distribuidoraResource import DistribuidoraResource,ObtenerDistribuidorasResource,DistribuidoraID

from resources.grupoExperimentalResource import GrupoExperimental, GruposExperimentales
from resources.jaulaResource import Jaula, JaulasSinProyecto, JaulasDelProyecto,BlogJaula,BorrarBlogJaula
from resources.fuenteExperimentalResource import FuenteExperimental
from resources.animalResource import  Animal, Animales, AnimalesSinJaula, AnimalesDeLaJaula

from resources.espacioFisicoResource import EspacioFisico,EspacioFisicoID
api = Api()
#Espacio fisico
EspacioFisico

api.add_resource(EspacioFisico, '/api/v1/espacioFisico')

api.add_resource(EspacioFisicoID, '/api/v1/espacioFisico/<int:id_espacioFisico>')


#permisos
api.add_resource(ObtenerPermisoPorId, '/api/v1/permiso/<int:id_permiso>')
api.add_resource(Permisos, '/api/v1/permisos')

#usuarios
api.add_resource(ObtenerUsuariosResource, '/api/v1/usuarios')
api.add_resource(UsuarioResource, '/api/v1/usuario')
api.add_resource(UsuarioID, '/api/v1/usuario/<int:id_usuario>')
api.add_resource(ObtenerUsuariosParaProyecto, '/api/UsuariosParaProyecto')

#proyectos
api.add_resource(Proyectos, '/api/v1/proyectos')
api.add_resource(NuevoProyecto, '/api/v1/nuevoProyecto')
api.add_resource(ProyectoID, '/api/v1/proyecto/<int:id_proyecto>')
api.add_resource(CerrarProyecto, '/api/v1/cerrarProyecto')
api.add_resource(ModificarProyecto, '/api/v1/modificarProyecto')
api.add_resource(ObtenerUsuariosProyecto, '/api/v1/obtenerUsuariosProyecto/<int:id_proyecto>')

#Grupo de trabajo
api.add_resource(GrupoDeTrabajo,'/api/v1/grupoDeTrabajo')
api.add_resource(GruposDeTrabajo, '/api/v1/gruposDeTrabajo')
api.add_resource(GrupoDeTrabajoID, '/api/v1/grupoDeTrabajo/<int:id_grupoDeTrabajo>')
api.add_resource(RenombrarJefeGrupo, '/api/v1/nuevoJefeDeGrupo') # ver si se queda o no 

#stock
api.add_resource(ObtenerProductosStock, '/api/v1/obtenerStock/<int:id_grupoDeTrabajo>/<int:id_espacioFisico>')
api.add_resource(ProductoEnStock, '/api/v1/productoEnStock')
api.add_resource(BorrarTodoStock, '/api/v1/borrar/<int:id_grupoDeTrabajo>')
api.add_resource(ConsumirStockResource, '/api/v1/consumirStock')
api.add_resource(ProductoEnStockID, '/api/v1/stock/<int:id_productoEnStock>/<int:id_productos>')

#producto
api.add_resource(ProductoResource, '/api/v1/producto')
api.add_resource(ObtenerProductosResource, '/api/v1/getProductos')
api.add_resource(ProductoID, '/api/v1/producto/<int:id_producto>')
api.add_resource(ArchivoProducto, '/api/v1/producto/subirArchivo/<int:id_producto>')

#distribuidora
api.add_resource(DistribuidoraResource, '/api/v1/distribuidora')
api.add_resource(ObtenerDistribuidorasResource, '/api/v1/getDistribuidoras')
api.add_resource(DistribuidoraID, '/api/v1/distribuidora/<int:id_distribuidora>')


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
api.add_resource(Jaula, '/api/v1/jaula/<int:id_jaula>', endpoint="jaula_por_id")
api.add_resource(Jaula, '/api/v1/asignarJaulaAProyecto', endpoint="asignar_jaula_a_proyecto")
api.add_resource(Jaula, '/api/v1/nuevaJaula', endpoint="nueva_jaula")
api.add_resource(Jaula, '/api/v1/bajarJaula/<int:id_jaula>', endpoint="bajar_jaula")
api.add_resource(JaulasSinProyecto, '/api/v1/jaulasDisponibles', endpoint="jaulas_disponibles")
api.add_resource(JaulasDelProyecto, '/api/v1/proyecto/<int:id_proyecto>/jaulasDelProyecto', endpoint="jaulas_del_proyecto")
api.add_resource(BlogJaula, '/api/v1/proyecto/blogJaula')
api.add_resource(BorrarBlogJaula, '/api/v1/proyecto/borrarBlogJaula/<int:id_jaula>/<int:id_blog>' )

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

#contenedor
api.add_resource(Contenedor, '/api/v1/contenedores', endpoint='contenedores')
api.add_resource(Contenedor, '/api/v1/nuevoContenedor', endpoint='nuevo_contenedore')
api.add_resource(ContenedorProyecto, '/api/v1/contenedoresDelProyecto', endpoint='contenedores_del_proyecto')
api.add_resource(ContenedorProyecto, '/api/v1/asignarProyectoAlContenedor', endpoint='asignar_proyecto_al_contenedor')
api.add_resource(ContenedorParent, '/api/v1/subcontenedores', endpoint='subcontenedores')
api.add_resource(ContenedorParent, '/api/v1/asignarParentAContenedores', endpoint='asignar_parent_a_contenedores')