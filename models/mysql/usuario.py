import sqlite3
from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, Integer, String, Text, Float, Boolean
from db import db
from models.mysql.permiso import Permiso

permisoXUsuario = db.Table('permisosxUsuarios', 
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id')),
    db.Column('permiso_id', db.Integer, db.ForeignKey('permisos.id_permiso'))
    )

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8','mysql_collate':'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60))
    nombre = db.Column(String(30))
    password = db.Column(String(80))
    habilitado = db.Column(db.Boolean, default = True, nullable=True)
    direccion = db.Column(String(50))
    telefono = db.Column(String(120))
    permisos = db.relationship('Permiso',secondary =permisoXUsuario, backref = db.backref('permisos'),lazy = 'dynamic')
    id_grupoDeTrabajo =  db.Column(db.Integer,default = 0)
    esJefeDe = db.Column(db.Integer,default = 0)
    
    def __init__(self, nombre, email, password,direccion,telefono,permisos,id_grupoDeTrabajo,esJefeDe):
        from servicios.permisosService import PermisosService
        self.nombre = nombre
        self.email = email
        self.password = password
        self.direccion = direccion
        self.telefono = telefono
        self.permisos = PermisosService.permisosById(permisos)
        self.id_grupoDeTrabajo =id_grupoDeTrabajo
        self.esJefeDe = esJefeDe


    

