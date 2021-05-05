from db import db
import json
from models.mysql.usuario import Permiso,PermisoSchema
from marshmallow import Schema, ValidationError
from flask import jsonify, request



class PermisosService():
    @classmethod
    def json(cls,datos):
        return jsonify( PermisoSchema().dump(datos))

    @classmethod
    def find_by_id(cls, _id_permiso):
        return Permiso.query.filter_by(id_permiso=_id_permiso).first()
        
    @classmethod
    def all_permisos(cls):
        permisos = Permiso.query.all()
        return jsonify(PermisoSchema().dump(permisos, many=True))


    @classmethod
    def permisosById(cls,permisosDict):
        '''recibe una lista de este estilo [{'id':1, 'descripcion':"asd},{'id':3, 'descripcion':"asd}]
        devuelve none si no encuentra todos los objetos de la lista en la base o una lista con los objetos 
        permisos de la base correspondients a esa id, este servicio lo usa nuevoUsuario()
        '''
        permisos = []
        print("entro a ver permisos")
        for dictonary in permisosDict:
            for key,value in dictonary.items():
                permiso = cls.find_by_id(value)
                if(permiso):
                    permisos.append(permiso)
        if(len(permisos) == len(permisosDict) and len(permisos)>0):
            return permisos
        return None

    @classmethod
    def obtenerPermisoPorId(cls,id_permiso):
        permiso = PermisosService.find_by_id(id_permiso)
        if permiso : 
            return PermisosService.json(permiso)
        return {'error':'No existen permisos con esa id'},400

