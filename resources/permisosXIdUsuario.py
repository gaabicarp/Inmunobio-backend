from models.usuario import Usuario
from flask_restful import Resource,Api
from flask_jwt import jwt_required
from flask import jsonify

class PermisosXIdUsuario(Resource):
	def get(self, id):
		#no hice la busqueda por username, me parecio mejor hacerla por id ya que es unico ->VER
		usuario = Usuario.find_by_id(id)
		permisos = {}
		if usuario:
		
			for permiso in usuario.id_permisos:
				permisos[permiso.id] = permiso.descripcion      
			return jsonify(permisos)
				
		return permisos, 404


