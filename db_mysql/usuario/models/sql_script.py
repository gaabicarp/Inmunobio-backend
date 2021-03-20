from flask import Flask
from app import db
from .usuario import *

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

        emmanuel = Usuario('Emmanuel', 'q1w2e3r4', 'Dirección 1', '12312121')
        naye = Usuario('Naye', 'q1w2e3r4','Dirección 2', '12312121')
        db.session.add_all([emmanuel, naye])
        db.session.commit()

        superusuarios.permisos.append(emmanuel)
        db.session.add(superusuarios)
        db.session.commit()
        superusuarios.permisos.append(naye)
        db.session.add(superusuarios)
        db.session.commit()
