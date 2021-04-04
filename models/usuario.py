import sqlite3
from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, Integer, String, Text, Float, Boolean
from db import db
from flask import jsonify

permisoXUsuario = db.Table('permisosxUsuarios', 
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id')),
    db.Column('permiso_id', db.Integer, db.ForeignKey('permisos.id'))
    )

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8','mysql_collate':'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    mail = db.Column(db.String(60))
    nombre = db.Column(String(30))
    password = db.Column(String(30))
    habilitado = db.Column(db.Boolean, default = True, nullable=True)
    direccion = db.Column(String(50))
    telefono = db.Column(String(120))
    id_permisos = db.relationship('Permiso',secondary =permisoXUsuario, backref = db.backref('permisos'),lazy = 'dynamic')
    
    def __init__(self, nombre, username, mail, password,direccion,telefono):
        self.nombre = nombre
        self.username = username
        self.mail = mail
        self.password = password
        self.direccion = direccion
        self.telefono = telefono

        
        
    def __repr__(self):
        return f"{self.id}||Nombre:{self.nombre} \r\n direccion:{self.direccion} \r\n  Telefono:{self.telefono} \r\n Username: {self.username} \r\n password: {self.password}, Permisos: {self.id_permisos[0]}"

    def json(self):
        usuarioSchema = UsuarioSchema()
        return jsonify(usuarioSchema.dump(self))

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
        
    @classmethod
    def find_usuarios_Habilitados(cls):
        return  cls.query.filter_by(habilitado=1).all()
    
    @classmethod
    def find_usuarios_Proyecto(cls,idPermiso):
        return Usuario.query.filter(~Usuario.id_permisos.any(Permiso.id.in_([idPermiso])))
     
        



class Permiso(db.Model):
    
    __tablename__='permisos'
    __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8','mysql_collate':'utf8_general_ci' }
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(String(70))

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        return f"El permiso es {self.descripcion} y tiene su número de id es {self.id}"
    
    def json(self):
        permisoSchema = PermisoSchema()
        return jsonify(permisoSchema.dump(self))

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
        
    @classmethod
    def all_permisos(cls):
        permisos = cls.query.all()
        return jsonify(Permisoschema().dump(permisos, many=True))


from marshmallow import Schema, fields
class PermisoSchema(Schema):
    id = fields.Str()
    descripcion = fields.Str()

class UsuarioSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str()
    mail = fields.Str()
    nombre = fields.Str()
    password = fields.Str()
    habilitado = fields.Int()
    direccion = fields.Str()
    telefono = fields.Str()
    id_permisos = fields.Nested(PermisoSchema, many=True)
