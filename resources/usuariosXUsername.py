from models.usuario import Usuario
from flask_restful import Resource,Api
from flask_jwt import jwt_required


class UsuarioxUsername(Resource):
	@jwt_required()
	def get(self, username):
		#usuario = Usuario.query.filter_by(username = username).first()
		usuario = Usuario.find_by_username(username)
		if usuario:
			return usuario.json()
		return {'name': 'None'},404


