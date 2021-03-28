from flask_restful import Resource,Api
from resources.usuarios import Usuarios,UsuarioxUsername,UsuariosXIdUsuario,NuevoUsuario, ActualizarPermisos

api = Api()

api.add_resource(Usuarios, '/api/usuarios')
api.add_resource(UsuarioxUsername, '/api/usuario/<string:username>')
api.add_resource(UsuariosXIdUsuario, '/api/usuario/<int:id>')
api.add_resource(NuevoUsuario, '/api/usuario/put')
api.add_resource(ActualizarPermisos, '/api/usuario/actualizarPermisos')
