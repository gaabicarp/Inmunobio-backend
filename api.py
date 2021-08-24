from flask_restful import Api

from resources.usuariosResource import  ObtenerUsuariosResource,UsuarioResource, UsuarioID,ObtenerUsuariosParaProyecto, Logins
from resources.proyectoResource import *
from resources.permisosResource import Permisos,ObtenerPermisoPorId
from resources.grupoDeTrabajoResource import GrupoDeTrabajoID,GrupoDeTrabajo,GruposDeTrabajo,RenombrarJefeGrupo
from resources.experimentoResource import TodosLosExperimentos,ExperimentoResource, ExperimentoMuestra,ObtenerBlogsExp,Experimentos, CerrarExperimento
from resources.contenedorResource import Contenedor, ContenedorProyecto, ContenedorParent,ContenedorProyectoId

from resources.grupoExperimentalResource import GrupoExperimental, GruposExperimentales, DividirGrupoExperimental
from resources.stockResource import ObtenerProductosStock,ProductoEnStock,BorrarTodoStock,ConsumirStockResource,ProductoEnStockID
from resources.productoResource import ProductoEnStockDeGrupos,ProductoResource,ObtenerProductosResource,ProductoID,ArchivoProducto
from resources.distribuidoraResource import DistribuidoraResource,ObtenerDistribuidorasResource,DistribuidoraID

from resources.grupoExperimentalResource import GrupoExperimental, GruposExperimentales
from resources.jaulaResource import JaulasBlogs,JaulaXId,ObtenerBlogsJaula,Jaula, JaulasSinProyecto, JaulasDelProyecto,BlogJaula,BorrarBlogJaula,Jaulas
from resources.fuenteExperimentalResource import FuenteExperimental,FuentesExperimentalesPorId,FuentesExperimentalesPorProyecto
from resources.animalResource import  Animal, Animales, AnimalesSinJaula, AnimalesDeLaJaula, AnimalesProyecto
from resources.muestraResource import BorraMuestras,MuestrasPorIDFuente,Muestra, MuestraGrupoExperimental, MuestraProyecto
from resources.animalResource import  Animal, Animales, AnimalesSinJaula, AnimalesDeLaJaula
from resources.espacioFisicoResource import EspaciosFisicos,EspacioFisico,EspacioFisicoID,CrearBlogEspacioFisico,BorrarBlogEspacioFisico,ObtenerBlogsEspFisico
from resources.herramientaResource import HerramientaResource,HerramientaPorId,Herramientas,BorrarBlogHeramienta,BlogHerramientaXId,CrearBlogHerramientas
from resources.datosResource import DatosResourceMongo,DatosResourceMysql
api = Api()

#datos
api.add_resource(DatosResourceMongo, '/api/v1/llenarBaseMongo')
api.add_resource(DatosResourceMysql, '/api/v1/llenarBaseMysql')

#Espacio fisico
api.add_resource(EspacioFisico, '/api/v1/espacioFisico')
api.add_resource(EspacioFisicoID, '/api/v1/espacioFisico/<int:id_espacioFisico>')
api.add_resource(EspaciosFisicos, '/api/v1/espaciosFisicos')
api.add_resource(BorrarBlogEspacioFisico, '/api/v1/borrarBlogEspacio/<int:id_espacioFisico>/<int:id_blog>')
api.add_resource(CrearBlogEspacioFisico, '/api/v1/crearBlogEspacio')
api.add_resource(ObtenerBlogsEspFisico, '/api/v1/blogsEspacio')

#permisos
api.add_resource(ObtenerPermisoPorId, '/api/v1/permiso/<int:id_permiso>')
api.add_resource(Permisos, '/api/v1/permisos')

#usuarios
api.add_resource(ObtenerUsuariosResource, '/api/v1/usuarios')
api.add_resource(UsuarioResource, '/api/v1/usuario')
api.add_resource(UsuarioID, '/api/v1/usuario/<int:id_usuario>')
api.add_resource(ObtenerUsuariosParaProyecto, '/api/v1/usuariosParaProyecto')
api.add_resource(Logins, '/api/v1/login', endpoint='login' )
api.add_resource(Logins, '/api/v1/prueba', endpoint='login_prueba' )

#proyectos
api.add_resource(Proyectos, '/api/v1/proyectos')
api.add_resource(NuevoProyecto, '/api/v1/nuevoProyecto')
api.add_resource(ProyectoID, '/api/v1/proyecto/<int:id_proyecto>')
api.add_resource(CerrarProyecto, '/api/v1/cerrarProyecto')
api.add_resource(ModificarProyecto, '/api/v1/modificarProyecto')
api.add_resource(ObtenerUsuariosProyecto, '/api/v1/obtenerUsuariosProyecto/<int:id_proyecto>')
api.add_resource(ObtenerBlogsProyecto, '/api/v1/blogsProyecto')
api.add_resource(NuevoBlogProyecto, '/api/v1/crearblogProyecto')
api.add_resource(ObtenerProyectoDeUsuario, '/api/v1/proyectosDeUsuario/<int:id_usuario>')


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
api.add_resource(ProductoEnStockDeGrupos, '/api/v1/gruposConStock/<int:id_producto>')

#distribuidora
api.add_resource(DistribuidoraResource, '/api/v1/distribuidora')
api.add_resource(ObtenerDistribuidorasResource, '/api/v1/getDistribuidoras')
api.add_resource(DistribuidoraID, '/api/v1/distribuidora/<int:id_distribuidora>')

#Experimento
api.add_resource(Experimentos, '/api/v1/proyecto/<int:idProyecto>/experimentos', endpoint='experimentos')
api.add_resource(ExperimentoResource, '/api/v1/experimento/<int:idExperimiento>', endpoint='experimento')
api.add_resource(ExperimentoResource, '/api/v1/nuevoExperimento', endpoint='nuevo_experimento')
api.add_resource(ExperimentoMuestra, '/api/v1/experimento/<int:idExperimento>/muestra/<int:idMuestra>', endpoint='remover_muestraExterna_de_experimento')
api.add_resource(CerrarExperimento, '/api/v1/cerrarExperimento', endpoint='cerrar_experimento')
api.add_resource(ExperimentoResource, '/api/v1/modificarExperimento', endpoint='modificar_experimento')
api.add_resource(ExperimentoMuestra, '/api/v1/agregarMuestrasExternasAlExperimento', endpoint='agregar_muestras_externas_al_experimento')
#api.add_resource(BlogExperimento, '/api/v1/nuevoBlogExperimento', endpoint='nuevo_blog_exp')
api.add_resource(ObtenerBlogsExp, '/api/v1/blogExperimento', endpoint='obtener_blog_exp')
api.add_resource(TodosLosExperimentos, '/api/v1/experimentos') #para testear

#Grupo Experimental
api.add_resource(GrupoExperimental, '/api/v1/grupoExperimental/<int:idGrupoExperimental>', endpoint='grupo_experimental')
api.add_resource(GrupoExperimental, '/api/v1/nuevoGrupoExperimental', endpoint='nuevo_grupo_experimental')
api.add_resource(GruposExperimentales, '/api/v1/experimento/<int:idExperimento>/gruposExperimentales', endpoint='grupos_experimentales_del_experimento')
api.add_resource(DividirGrupoExperimental, '/api/v1/dividirGrupoExperimental', endpoint='dividir_grupo_experimental')
api.add_resource(GrupoExperimental, '/api/v1/borrarGrupoExperimental/<int:idGrupoExperimental>', endpoint='borrar_grupo_experimental')

#Jaula
api.add_resource(Jaula, '/api/v1/nuevaJaula', endpoint="nueva_jaula")
api.add_resource(Jaula, '/api/v1/modificarJaula', endpoint="modificar_jaula")
api.add_resource(Jaula, '/api/v1/bajarJaula/<int:id_jaula>', endpoint="bajar_jaula")
api.add_resource(JaulasSinProyecto, '/api/v1/jaulasDisponibles', endpoint="jaulas_disponibles")
api.add_resource(JaulasDelProyecto, '/api/v1/proyecto/<int:idProyecto>/jaulasDelProyecto', endpoint="jaulas_del_proyecto")
api.add_resource(JaulasDelProyecto, '/api/v1/asignarJaulaAProyecto', endpoint="asignar_jaula_a_proyecto")
api.add_resource(BlogJaula, '/api/v1/proyecto/blogJaula')
api.add_resource(ObtenerBlogsJaula, '/api/v1/proyecto/blogsJaula')
#api.add_resource(BorrarBlogJaula, '/api/v1/proyecto/borrarBlogJaula/<int:id_jaula>/<int:id_blog>' )
api.add_resource(Jaulas, '/api/v1/jaulas')
api.add_resource(JaulaXId, '/api/v1/jaula/<int:id_jaula>', endpoint="jaula_por_id")
api.add_resource(JaulasBlogs, '/api/v1/blogsJaulas')

#FuenteExperimental
api.add_resource(FuenteExperimental, '/api/v1/fuenteExperimental/<string:codigo>', endpoint="fuente_experimental")
api.add_resource(FuenteExperimental, '/api/v1/nuevasFuentesExperimentales', endpoint="nuevas_fuentes_experimentales")
api.add_resource(FuentesExperimentalesPorId, '/api/v1/fuenteExperimental/<int:id_fuente>', endpoint="fuentes_por_id")
api.add_resource(FuentesExperimentalesPorProyecto, '/api/v1/fuentesExperimentales/<int:id_proyecto>', endpoint="fuentes_de_proyecto")

#Animal
api.add_resource(Animal, '/api/v1/animal/<int:idAnimal>', endpoint="animal")
api.add_resource(Animal, '/api/v1/bajaAnimal/<int:idAnimal>', endpoint="baja_animal")
api.add_resource(Animal, '/api/v1/nuevoAnimal', endpoint="nuevo_animal")
api.add_resource(Animales, '/api/v1/animales', endpoint="animales")
#api.add_resource((Animales))
api.add_resource(AnimalesSinJaula, '/api/v1/animalesSinJaula', endpoint="animales_sin_jaula")
api.add_resource(AnimalesDeLaJaula, '/api/v1/jaula/<int:idJaula>/animales', endpoint="animales_de_la_jaula")
api.add_resource(AnimalesDeLaJaula, '/api/v1/asignarJaulas', endpoint="asignar_jaulas")
api.add_resource(AnimalesProyecto, '/api/v1/proyecto/<int:idProyecto>/animales', endpoint="animales_del_proyecto")

#contenedor
api.add_resource(Contenedor, '/api/v1/contenedores', endpoint='contenedores')
api.add_resource(Contenedor, '/api/v1/nuevoContenedor', endpoint='nuevo_contenedores')
api.add_resource(Contenedor, '/api/v1/modificarContenedor', endpoint='modificar_contenedor')
api.add_resource(Contenedor, '/api/v1/eliminarContenedor/<int:idContenedor>', endpoint='eliminar_contenedor')
api.add_resource(ContenedorProyecto, '/api/v1/contenedoresDelProyecto', endpoint='contenedores_del_proyecto')
api.add_resource(ContenedorProyecto, '/api/v1/asignarProyectoAlContenedor', endpoint='asignar_proyecto_al_contenedor')
api.add_resource(ContenedorParent, '/api/v1/subcontenedores', endpoint='subcontenedores')
api.add_resource(ContenedorParent, '/api/v1/asignarParentAContenedor', endpoint='asignar_parent_a_contenedor')
api.add_resource(ContenedorProyectoId, '/api/v1/contenedoresDelProyecto/<int:id_proyecto>')

#Muestra
api.add_resource(Muestra, '/api/v1/muestra/<int:idMuestra>', endpoint='muestra')
api.add_resource(Muestra, '/api/v1/nuevaMuestra', endpoint='nueva_muestra')
api.add_resource(Muestra, '/api/v1/modificarMuestra', endpoint='modificar_muestra')
api.add_resource(Muestra, '/api/v1/bajarMuestra/<int:idMuestra>', endpoint='bajar_muestra')
api.add_resource(MuestraGrupoExperimental, '/api/v1/grupoExperimental/<int:idGrupoExperimental>/muestras', endpoint='muestras_grupo_experimental')
api.add_resource(MuestraProyecto, '/api/v1/proyecto/<int:idProyecto>/muestras', endpoint='muestras_proyecto')
api.add_resource(MuestrasPorIDFuente, '/api/v1/muestras/<int:idFuenteExperimental>')
api.add_resource(BorraMuestras, '/api/v1/muestras/borrar')


#Herramientas
api.add_resource(HerramientaResource, '/api/v1/herramienta')
api.add_resource(HerramientaPorId, '/api/v1/herramienta/<int:id_herramienta>')
api.add_resource(Herramientas, '/api/v1/herramientas/')
api.add_resource(BorrarBlogHeramienta, '/api/v1/blogHerramienta/<id_herramienta>/<int:id_blog>')
api.add_resource(BlogHerramientaXId, '/api/v1/blogHerramienta')
api.add_resource(CrearBlogHerramientas, '/api/v1/crearBlogHerramienta')