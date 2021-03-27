from models.usuario import Usuario
from flask_restful import Resource,Api
from flask_jwt import jwt_required
from flask import jsonify,request
from db import db

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
   
    
