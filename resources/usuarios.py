from models.usuario import Usuario
from flask_restful import Resource,Api
from flask_jwt import jwt_required
from flask import jsonify, request
class Usuarios(Resource):

    def get(self):
        usuarios = Usuario.query.limit(2).all()
        
        if usuarios:
            return [usuario.json() for usuario in usuarios]
        return {'name': 'None'},404

class UsuariosXIdUsuario(Resource):

    @jwt_required()
    def get(self, id):
        usuario = Usuario.find_by_id(id)
        if usuario:
            return usuario.json()
        return {'name': 'None'},404
    
    @jwt_required()
    def post(self,id):

        datos = request.get_json(silent=True)
        if (datos):
            nombre = datos['nombre']
            username = datos['username']
            password = datos['password']
            mail = datos['mail']
            direccion = datos['direccion']
            telefono = datos['telefono']
            usuario = Usuario(nombre , username , mail,password,direccion ,telefono )
            db.session.add(usuario)
            db.session.commit()
            return {'Status':'ok'}
        return {'name': 'None'},404
    @jwt_required()
    def put(self,id):
        modificaciones = request.get_json()
        #aca los parametros pueden ser direccion y/o telefono y/o mail y/o contraseña
        usuario = Usuario.find_by_id(id)
        if usuario:
            for clave,valor in modificaciones.items():
                if hasattr(usuario, clave):
                    setattr(usuario, clave, valor)
            db.session.commit()
            #no esta contemplando que esa clave exista o no->solucionado con hasattr pero meh
            return {'Status':'ok'}
        return {'name': 'None'},404
    
    
""" class PermisosXIdUsuario(Resource):
	@jwt_required()
	def get(self, id):
		no hice la busqueda por username, me parecio mejor hacerla por id ya que es unico ->VER
		usuario = Usuario.find_by_id(id)
		permisos = {}
		if usuario:
		
			for permiso in usuario.id_permisos:
				permisos[permiso.id] = permiso.descripcion      
			return jsonify(permisos)
				
		return  {'name': 'None'},404 """


class NuevoUsuario(Resource):
    
    @jwt_required()
    def post(self):
        datos = request.get_json(silent=True)
        if (datos):
            nombre = datos['nombre']
            username = datos['username']
            password = datos['password']
            mail = datos['mail']
            direccion = datos['direccion']
            telefono = datos['telefono']
            usuario = Usuario(nombre , username , mail,password,direccion ,telefono )
            db.session.add(usuario)
            db.session.commit()
            return {'Status':'ok'},200
        return {'name': 'None'},404
   
    
class UsuarioxUsername(Resource):
	@jwt_required()
	def get(self, username):
		#usuario = Usuario.query.filter_by(username = username).first()
		usuario = Usuario.find_by_username(username)
		if usuario:
			return usuario.json()
		return {'name': 'None'},404

