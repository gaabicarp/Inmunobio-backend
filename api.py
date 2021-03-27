from flask_restful import Resource,Api
from resources.usuarios import Usuarios
from resources.usuariosXUsername import UsuarioxUsername
from resources.permisosXIdUsuario import PermisosXIdUsuario
from resources.usuariosXIdUsuario import UsuariosXIdUsuario
from resources.nuevoUsuario import NuevoUsuario
api = Api()
#nojwt = JWT(app, authenticate, identity) 

api.add_resource(Usuarios, '/api/usuarios')
api.add_resource(UsuarioxUsername, '/api/usuario/<string:username>')
api.add_resource(PermisosXIdUsuario, '/api/permisos/<int:id>')
api.add_resource(UsuariosXIdUsuario, '/api/usuario/get/<int:id>')
api.add_resource(NuevoUsuario, '/api/usuario/put')

#aca le pedimos la id para crear?? -> ver como separar las rutas o mejorar esto