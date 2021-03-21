from flask import Flask
from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, Integer, String, Text, Float, Boolean
from app import db

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
    contrasenia = db.Column(String(30))
    habilitado = db.Column(db.Boolean, default = True, nullable=True)
    direccion = db.Column(String(50))
    telefono = db.Column(String(120))
    id_permisos = db.relationship('Permiso',secondary =permisoXUsuario, backref = db.backref('permisos'),lazy = 'dynamic')
    
    def __init__(self, nombre, username, mail, contrasenia,direccion,telefono):
        self.nombre = nombre
        self.username = username
        self.mail = mail
        self.contrasenia = contrasenia
        self.direccion = direccion
        self.telefono = telefono
        
    def __repr__(self):
        return f"{self.id}||Nombre:{self.nombre} \n direccion:{self.direccion} \n  Telefono:{self.telefono}"

    def json(self):
        return {
            'nombre':self.nombre,
            'username':self.username,
            'mail':self.mail,
            'contrasenia':self.contrasenia, 
            'habilitado':self.habilitado,
            'direccion':self.direccion,
            'telefono':self.telefono
            }
        
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
        return {'descripcion': self.descripcion}


