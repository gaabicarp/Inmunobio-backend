from db_mysql.usuario.models import Usuario
from flask_restful import Resource,Api



class UsuarioxUsername(Resource):
	def get(self, username):
		usuario = Usuario.query.filter_by(username = username).first()
		if usuario:
			return usuario.json()
		return {'name': 'None'},404
