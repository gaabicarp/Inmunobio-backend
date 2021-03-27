from models.usuario import Usuario
from flask_restful import Resource,Api
from flask_jwt import jwt_required
from flask import jsonify,request
from db import db

class UsuariosXIdUsuario(Resource):

    #@jwt_required()
    def get(self, id):
        usuario = Usuario.find_by_id(id)
        if usuario:
            return usuario.json()
        return {'name': 'None'},404
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
    
