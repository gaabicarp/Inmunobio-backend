
from db import db

class Permiso(db.Model):
    
    __tablename__='permisos'
    __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8','mysql_collate':'utf8_general_ci' }
    id_permiso = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(70))

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        return f"El permiso es {self.descripcion} y  su número de id es {self.id_permiso}"