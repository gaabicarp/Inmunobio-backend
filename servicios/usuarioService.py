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
            cls.validarTipoDatos(modificaciones) # falta ver extra fields
            cls.updateAtributes(usuario,modificaciones)
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages}, 404

    @classmethod
    def asignarPermisos(cls,usuario,permisosDicts):
        '''recibe una lista con diccionarios de permisos y un usuario de la base
        si pudo encontrar los permisos en la base actualiza al usuario, sino devuelve
        mensaje de error.'''
        permisosObject = PermisosService.permisosById(permisosDicts)
        if (permisosObject):
            usuario.setPermiso(permisosObject)
            db.session.add(usuario)
            db.session.commit()
            return {'Status':'ok'},200
        return {'error': 'Permisos invalidos'},404
            

    @classmethod
    def nuevoUsuario(cls,datos):
        #minimo un permiso  el 5, aun no esta validado , solo valida que sean permisos que existen
        try:
            usuario = UsuarioNuevoSchema().load(datos) 
            return cls.asignarPermisos(usuario,datos['id_permisos'])
        except ValidationError as err:
            return {'error': err.messages},404

    @classmethod
    def find_by_username(cls, username):
        return Usuario.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return Usuario.query.filter_by(id=_id).first()
        
    @classmethod
    def find_usuarios_Habilitados(cls):
        return  Usuario.query.filter_by(habilitado=1).all()
    
    @classmethod
    def usuariosSinElPermiso(cls,idPermiso):
        user = Usuario.query.filter(~Usuario.id_permisos.any(Permiso.id.in_([idPermiso])))
        if (user):
            return cls.jsonMany(user)
        return {}
    
    def json(datos):
        return UsuarioSchema().dump(datos)

    def jsonMany(datos):
        return jsonify(UsuarioSchema().dump(datos,many=True))    
        
    
    def validarTipoDatos(datos):
        return UsuarioSchemaModificar().load(datos)

    def busquedaValidada(datos):
        '''recibe un diccionario , verifica que se pase como key una id de usuario,
        y devuelve el usuario habilitado en la base con esa id o nada si no existe o esta deshabilitado
        '''
        if('id' in datos):
            usuario = UsuarioService.find_by_id(datos['id'])
            if (usuario and usuario.habilitado):
                return usuario
            return None
        return None

    @classmethod
    def actualizarPermisos(cls,datos):
        try:
            UsuarioSchemaModificarPermisos().load(datos)
            print("se validaron sfiedls")
            usuario = cls.busquedaValidada(datos)
            print(usuario)
            if(usuario):
                print("asigno permisos")
                return cls.asignarPermisos(usuario,datos['id_permisos'])
            return {'error':'no existe el usuario'},404
        except ValidationError as err:
            return {'error': err.messages},404

    @classmethod
    def deshabilitarUsuario(cls,datos):
        """recibe un usuario valido y modifica su estado habilitado a false"""
        usuario = UsuarioService.busquedaValidada(datos)
        if(usuario):
            cls.updateAtributes(usuario,{'habilitado': False})
            return {'Status':'ok'},200
        return {'error':'No existe usuario'},404

