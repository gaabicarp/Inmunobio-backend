from db import db
import json
from models.mysql.permiso import Permiso
from flask import jsonify
from schemas.permisosSchema import PermisoSchema,PermisoExistenteSchema
from servicios.commonService import CommonService

class PermisosService():
    jefeDeGrupo = 3
    jefeProyecto = 4
    tecnico = 5
    
    @classmethod
    def json(cls,datos):
        return jsonify( PermisoSchema().dump(datos))

    @classmethod
    def find_by_id(cls, _id_permiso):
        permiso= Permiso.query.filter_by(id_permiso=_id_permiso).first()
        if not permiso: 
            raise Exception(f"No hay permisos asociados con id {_id_permiso}")
        return permiso
        
    @classmethod
    def all_permisos(cls):
        permisos = Permiso.query.all()
        return CommonService.jsonMany(permisos,PermisoExistenteSchema)

    @classmethod
    def permisosDefault(cls,permisosDicts):
        if not cls.tieneElPermiso(permisosDicts,cls.tecnico): permisosDicts.append(cls.find_by_id(cls.tecnico))
        return permisosDicts

    @classmethod
    def permisosById(cls,permisosDict):
        return cls.permisosDefault(list(set(map(lambda x : cls.find_by_id(x['id_permiso']), permisosDict))))

    @classmethod
    def obtenerPermisoPorId(cls,id_permiso):
        try:
            return CommonService.json(PermisosService.find_by_id(id_permiso),PermisoSchema)
        except Exception as err: return {'Error': err.message},400

    @classmethod
    def tieneElPermiso(cls, permisos, idPermiso):
        return any( permiso.id_permiso == idPermiso for permiso in permisos)
    
    @classmethod
    def esJefeDeProyecto(cls,usuario):
        if not cls.tieneElPermiso(usuario.permisos,cls.jefeProyecto): raise Exception(f"El usuario {usuario.nombre} no tiene permisos como Jefe De Proyecto id.{cls.jefeProyecto}")
