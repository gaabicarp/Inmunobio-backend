from flask_restful import Resource,Api
from resources.usuarios import Usuarios
from resources.usuariosXUsername import UsuarioxUsername
from resources.permisosXIdUsuario import PermisosXIdUsuario
api = Api()
#jwt = JWT(app, authenticate, identity) 

api.add_resource(Usuarios, '/api/usuarios')
api.add_resource(UsuarioxUsername, '/api/usuario/<string:username>')
api.add_resource(PermisosXIdUsuario, '/api/permisos/usuario/<int:id>')