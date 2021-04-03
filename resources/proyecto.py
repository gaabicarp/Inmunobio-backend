from models.mongo.proyecto import Proyecto
from flask_restful import Resource,Api
from flask_jwt import jwt_required
from flask import jsonify, request
from dateutil import parser
import json

class Proyectos(Resource):

    def get(self):
        proyectos = Proyecto.find_all()
        if proyectos:
           return proyectos 
        return {'name': 'None'},404

class NuevoProyecto(Resource):

    # @jwt_required()
    def post(self):
        datos = request.get_json()

        if (datos):
            nuevoProyecto = Proyecto()
            nuevoProyecto.nombre = datos['nombre']
            nuevoProyecto.descripcion = datos['descripcion']
            nuevoProyecto.montoInicial = datos['montoInicial']

            nuevoProyecto.guardar()
            return {'Status':'ok', 'Proyecto':nuevoProyecto.json()},200
        return {'name': datos},404