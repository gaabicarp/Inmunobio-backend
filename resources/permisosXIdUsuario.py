from models.usuario import Usuario, UsuarioSchema
from flask_restful import Resource,Api
from flask_jwt import jwt_required
from flask import request

class PermisosXIdUsuario(Resource):
	#@jwt_required()
	def get(self, id):
		#no hice la busqueda por username, me parecio mejor hacerla por id ya que es unico ->VER
		user_schema = UsuarioSchema()
		usuario = Usuario.find_by_id(id)
		return usuario.json()


