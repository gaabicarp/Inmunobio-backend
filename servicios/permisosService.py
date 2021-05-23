from db import db
import json
from models.mysql.permiso import Permiso
from marshmallow import Schema, ValidationError
from flask import jsonify, request
from schemas.permisosSchema import PermisoSchema
from servicios.commonService import CommonService
from exceptions.exception import ErrorPermisoInexistente
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
        return CommonService.jsonMany(permisos,PermisoSchema)


    @classmethod
    def permisosById(cls,permisosDict):
        '''recibe una lista de este estilo [{'id':1, 'descripcion':"asd},{'id':3, 'descripcion':"asd}]
        devuelve none si no encuentra todos los objetos de la lista en la base o una lista con los objetos 
        permisos de la base correspondients a esa id, este servicio lo usa nuevoUsuario()
        '''
        permisos = []
        print("entro a ver permisos")
        for dictonary in permisosDict:
            permiso = cls.find_by_id(dictonary['id_permiso'])
            if(permiso):
                permisos.append(permiso)
            else: raise ErrorPermisoInexistente(dictonary['id_permiso'])
        return permisos

    @classmethod
    def obtenerPermisoPorId(cls,id_permiso):
        permiso = PermisosService.find_by_id(id_permiso)
        if permiso : 
            return CommonService.json(permiso,PermisoSchema)
        return {'error':'No existen permisos con esa id'},400

