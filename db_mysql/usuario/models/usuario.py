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
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(String(30))
	contrasenia = db.Column(String(10))
	habilitado = db.Column(db.Boolean, default = True, nullable=True)
	direccion = db.Column(String(50))
	telefono = db.Column(String(120))
	apodo = db.Column(String(100))
	id_permisos = db.relationship('Permiso',secondary =permisoXUsuario, backref = db.backref('permisos'),lazy = 'dynamic')
	

	def __init__(self, nombre, contrasenia,direccion,telefono,apodo):
		self.nombre = nombre
		self.contrasenia = contrasenia
		self.direccion = direccion
		self.telefono = telefono
		self.apodo = apodo
		
	def __repr__(self):
		return f"{self.id}||Nombre:{self.nombre} \n direccion:{self.direccion} \n  Telefono:{self.telefono}"
		


class Permiso(db.Model):
    __tablename__ = 'permisos'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(String(30))

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        return f"El permiso es {self.descripcion} y tiene su número de id es {self.id}"


