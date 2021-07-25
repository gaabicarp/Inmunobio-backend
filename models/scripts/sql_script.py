import os
from schemas.proyectoSchema import ProyectoNuevoSchema
from flask import Flask
from app import db
from models.mysql.usuario import *
from models.mongo.proyecto import Proyecto
app = Flask(__name__)

class MysqlScript:

    def __init__(self):
        pass

    def ScriptLlenarTablas():
        superusuarios = Permiso('Superusuario')
        directorCentro = Permiso('Director de centro')
        jefe = Permiso('Jefe de grupo')
        directorProyecto = Permiso('Director de proyecto / bioterio')
        tecnico = Permiso('Técnico')
        db.session.add_all([superusuarios, directorCentro, jefe, directorProyecto, tecnico])
        db.session.commit()
        emmanuel = Usuario('Emmanuel', 'emmanuel@emmauel.com', 'q1w2e3r4', 'Dirección 1', '12312121',0)
        naye = Usuario('Naye', 'naye@naye.com', 'q1w2e3r455','Dirección 2', '12312121',0)
        db.session.add_all([emmanuel, naye])
        superusuarios.permisos.append(emmanuel)
        superusuarios.permisos.append(naye)
        tecnico.permisos.append(naye)
        db.session.add(superusuarios)
        db.session.add(tecnico)
        db.session.commit()