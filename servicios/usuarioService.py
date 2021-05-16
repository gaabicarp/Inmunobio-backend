from db import db
import json
from models.mysql.usuario import UsuarioSchema,UsuarioSchemaModificar,Usuario,UsuarioNuevoSchema,UsuarioSchemaModificarPermisos
from marshmallow import Schema, ValidationError
from flask import jsonify, request
from servicios.permisosService import PermisosService,Permiso


class UsuarioService():
    @classmethod
    def updateAtributes(cls,usuario,atributos):
        """recibe un diccionario con atributo - valor , si el usuario tiene esos atributos
        los actualiza y guarda los cambios enla base"""
        for clave,valor in atributos.items():
                if hasattr(usuario, clave) :
                    setattr(usuario, clave, valor)
        db.session.commit()

    @classmethod
    def modificarUsuario(cls,usuario,modificaciones):        
        try:
            cls.validarTipoDatos(modificaciones) 
            cls.updateAtributes(usuario,modificaciones)
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages}, 400

    @classmethod
    def asignarPermisos(cls,usuario,permisosDicts):
        '''recibe una lista con diccionarios de permisos y un usuario de la base
        si pudo encontrar los permisos en la base actualiza al usuario, sino devuelve
        mensaje de error.'''
        permisosObject = PermisosService.permisosById(permisosDicts)
        if (permisosObject is not None):
            usuario.setPermiso(permisosObject)
            db.session.add(usuario)
            db.session.commit()
            return {'Status':'ok'},200
        return {'error': 'Permisos invalidos'},400
            

    @classmethod
    def nuevoUsuario(cls,datos):
        #minimo un permiso  el 5, aun no esta validado , solo valida que sean permisos que existen
        try:
            usuario = UsuarioNuevoSchema().load(datos) 
            return cls.asignarPermisos(usuario,datos['id_permisos'])
        except ValidationError as err:
            return {'error': err.messages},400

    @classmethod
    def find_by_email(cls, _email):
        return Usuario.query.filter_by(email=_email).first()

    @classmethod
    def find_by_id(cls, _id):
        '''dada una id de usuario devuelve usuario si esta habilitado '''
        return Usuario.query.filter_by(id_usuario=_id,habilitado=True).first()
        
    @classmethod
    def findUsuariosHabilitados(cls):
        return  Usuario.query.filter_by(habilitado=1).all()
    
    @classmethod
    def usuariosSinElPermiso(cls,id_permiso):
        user = Usuario.query.filter(~Usuario.id_permisos.any(Permiso.id_permiso.in_([id_permiso])))
        if (user):
            return cls.jsonMany(user)
        return {}
    
    def json(datos):
        return UsuarioSchema().dump(datos)

    def jsonMany(datos):
        return jsonify(UsuarioSchema().dump(datos,many=True))    
        
    
    def validarTipoDatos(datos):
        print('entro a validar')
        return UsuarioSchemaModificar().load(datos)


    @classmethod
    def actualizarPermisos(cls,datos):
        try:
            UsuarioSchemaModificarPermisos().load(datos)
            usuario = cls.find_by_id(datos['id_usuario'])
            if(usuario):
                return cls.asignarPermisos(usuario,datos['id_permisos'])
            return {'error':'no existe el usuario'},400
        except ValidationError as err:
            return {'error': err.messages},400

    @classmethod
    def deshabilitarUsuario(cls,datos):
        """recibe un usuario valido y modifica su estado habilitado a false"""
        #agregar schema de id usuario para verificar que se pase
        usuario = UsuarioService.find_by_id(datos['id_usuario'])
        if(usuario):
            cls.updateAtributes(usuario,{'habilitado': False})
            return {'Status':'ok'},200
        return {'error':'No existe usuario'},400

