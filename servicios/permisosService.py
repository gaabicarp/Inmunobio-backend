from db import db
import json
from models.mysql.permiso import Permiso
from flask import jsonify
from schemas.permisosSchema import PermisoSchema,PermisoExistenteSchema
from servicios.commonService import CommonService
from exceptions.exception import ErrorPermisoInexistente,ErrorPermisoGeneral

class PermisosService():
    jefeDeGrupo = 4
    
    @classmethod
    def json(cls,datos):
        return jsonify( PermisoSchema().dump(datos))

    @classmethod
    def find_by_id(cls, _id_permiso):
        permiso= Permiso.query.filter_by(id_permiso=_id_permiso).first()
        if not permiso: 
            raise ErrorPermisoInexistente(_id_permiso)
        return permiso
        
    @classmethod
    def all_permisos(cls):
        permisos = Permiso.query.all()
        return CommonService.jsonMany(permisos,PermisoExistenteSchema)

    @classmethod
    def validarPermisos(cls,permisosDicts):
        if not any(permiso['id_permiso'] == 5 for permiso in permisosDicts): raise ErrorPermisoGeneral()

    @classmethod
    def permisosById(cls,permisosDict):
        #cls.validarPermisos(permisosDict) -> ya no lo validamos, sino que se agrega.
        return list(set(map(lambda x : cls.find_by_id(x['id_permiso']), permisosDict)))

    @classmethod
    def obtenerPermisoPorId(cls,id_permiso):
        try:
            return CommonService.json(PermisosService.find_by_id(id_permiso),PermisoSchema)
        except ErrorPermisoInexistente as err:
            return {'error': err.message},400

    @classmethod
    def tieneElPermiso(cls,usuario,idPermiso):
        return any( permiso.id_permiso == idPermiso for permiso in usuario.permisos)



