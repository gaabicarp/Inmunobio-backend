import sqlite3
from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, Integer, String, Text, Float, Boolean
from db import db
from marshmallow import Schema, fields, post_load, ValidationError


permisoXUsuario = db.Table('permisosxUsuarios', 
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id_usuario')),
    db.Column('permiso_id', db.Integer, db.ForeignKey('permisos.id_permiso'))
    )

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8','mysql_collate':'utf8_general_ci'}
    id_usuario = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60))
    nombre = db.Column(String(30))
    password = db.Column(String(30))
    habilitado = db.Column(db.Boolean, default = True, nullable=True)
    direccion = db.Column(String(50))
    telefono = db.Column(String(120))
    id_permisos = db.relationship('Permiso',secondary =permisoXUsuario, backref = db.backref('permisos'),lazy = 'dynamic')
    
    def __init__(self, nombre, email, password,direccion,telefono,id_permisos):
        self.nombre = nombre
        self.email = email
        self.password = password
        self.direccion = direccion
        self.telefono = telefono

    def __repr__(self):
        return f"{self.id_usuario}||Nombre:{self.nombre} \r\n direccion:{self.direccion} \r\n  Telefono:{self.telefono} \r\n  password: {self.password}, Permisos: {self.id_permisos[0]}"
    def setPermiso(self,permisos):
        self.id_permisos = permisos
    
        
class Permiso(db.Model):
    
    __tablename__='permisos'
    __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8','mysql_collate':'utf8_general_ci' }
    id_permiso = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(String(70))

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        return f"El permiso es {self.descripcion} y  su número de id es {self.id_permiso}"
    

class PermisoSchema(Schema):
    id_permiso = fields.Integer()
    descripcion = fields.Str()
   
class PermisoExistenteSchema(PermisoSchema):
    id_permiso = fields.Integer( 
        required=True,
        error_messages={"required": {"message": "Debe indicarse el id del permiso", "code": 400}},
    )
    descripcion = fields.Str( 
        required=True,
        error_messages={"required": {"message": "Debe indicarse la descripcion del permiso", "code": 400}},
    )
class UsuarioSchema(Schema):
    id_usuario = fields.Integer(dump_only=True)
    email = fields.Str()
    nombre = fields.Str()
    password = fields.Str()    
    habilitado = fields.Boolean(default=True)
    direccion = fields.Str()
    telefono = fields.Str()
    id_permisos = fields.Nested(PermisoSchema, many=True)

class UsuarioNuevoSchema(UsuarioSchema):
    email = fields.Str( 
        required=True,
        error_messages={"required": {"message": "Se necesita ingresar el mail", "code": 400}},
    )
    nombre = fields.Str( 
        required=True,
        error_messages={"required": {"message": "Se necesita ingresar el nombre del usuario", "code": 400}},
    )
    password = fields.Str(
         required=True,
        error_messages={"required": {"message": "Se necesita ingresar el password", "code": 400}},
    )
    direccion = fields.Str (
        required=True,
        error_messages={"required": {"message": "Se necesita ingresar la direccion", "code": 400}},
    )
    telefono = fields.Str( required=True,
        error_messages={"required": {"message": "Se necesita ingresar  el telefono", "code": 400}},
    )
    habilitado = fields.Int()
    id_permisos = fields.Nested(PermisoExistenteSchema, many=True, required=True,
        error_messages={"required": {"message": "Se necesita asignar permisos", "code": 400}},
    )
    @post_load
    def make_Usuario(self, data, **kwargs):
        return Usuario(**data)

class UsuarioSchemaModificar(Schema):
    """ class Meta:
        unknown = EXCLUDE """

    id_usuario = fields.Integer(load_only=True)
    email = fields.Str()
    password = fields.Str()    
    direccion = fields.Str()
    telefono = fields.Str()

class UsuarioSchemaModificarPermisos(UsuarioSchema):
    id_usuario = fields.Integer( 
        required=True,
        error_messages={"required": {"message": "Debe indicarse id Usuario", "code": 400}},
    )
    id_permisos = fields.Nested(PermisoSchema, many=True,required=True,
    error_messages={"required": {"message": "Debe indicarse permisos al Usuario", "code": 400}},
    )

