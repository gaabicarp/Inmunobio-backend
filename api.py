from flask_restful import Resource,Api
from resources.usuarios import Usuarios,UsuarioxUsername,UsuariosXIdUsuario,NuevoUsuario, ActualizarPermisos, UsuariosProyecto
from resources.proyecto import *

api = Api()

api.add_resource(Usuarios, '/api/usuarios')
api.add_resource(UsuarioxUsername, '/api/usuario/<string:username>')
api.add_resource(UsuariosXIdUsuario, '/api/usuario/<int:id>')
api.add_resource(NuevoUsuario, '/api/nuevoUsuario')
api.add_resource(UsuariosProyecto, '/api/usuariosProyecto')

api.add_resource(Proyectos, '/api/proyectos')
api.add_resource(NuevoProyecto, '/api/nuevoProyecto')
api.add_resource(ProyectoID, '/api/proyectoID')
api.add_resource(CerrarProyecto, '/api/cerrarProyecto')
api.add_resource(ModificarProyecto, '/api/modificarProyecto')