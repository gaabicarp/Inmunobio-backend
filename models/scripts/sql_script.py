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
        emmanuel = Usuario('Emmanuel',  'emmanuel@emmauel.com', 'q1w2e3r4', 'Dirección 1', '12312121',0)
        naye = Usuario('Naye', 'naye@naye.com', 'q1w2e3r455','Dirección 2', '12312121',0)
        db.session.add_all([emmanuel, naye])
        superusuarios.permisos.append(emmanuel)
        superusuarios.permisos.append(naye)
        tecnico.permisos.append(naye)
        db.session.add(superusuarios)
        db.session.add(tecnico)
        db.session.commit()

    def leerArchivoCSV(self, fileName):
        file = open(f'./CSV/{fileName}', 'r')
        next(file)
        for linea in file:
            self.cargarProyecto(linea)
    
    def cargarProyecto(self, datos):
        valores = datos.split(';')
        print(f'Se carga el proyecto: {valores[0]}')
        proyecto = Proyecto()
        proyecto.id_proyecto = valores[0]
        proyecto.nombre = valores[1]
        proyecto.descripcion = valores[2]
        proyecto.participantes = valores[3]
        proyecto.idDirectorProyecto = valores[4]
        proyecto.fechaInicio = valores[5]
        proyecto.fechaFinal = valores[6]
        proyecto.montoInicial = valores[7]
        proyecto.conclusion = valores[8]
        proyecto.save()


