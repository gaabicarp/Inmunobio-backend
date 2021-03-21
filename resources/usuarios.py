from models.usuario import Usuario
from flask_restful import Resource,Api

class Usuarios(Resource):

    def get(self):
        usuarios = Usuario.query.limit(2).all()
        
        if usuarios:
            return [usuario.json() for usuario in usuarios]
        return {'name': 'None'},404