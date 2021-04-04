from models.mongo.proyecto import Proyecto, ProyectoSchema
from flask_restful import Resource,Api
from flask_jwt import jwt_required
from flask import jsonify, request
from dateutil import parser
import json
from marshmallow import ValidationError
from pprint import pprint
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
        if datos:
            miembros = Proyecto.agregarMiembros()
            for miembro in miembros :
                print(miembro)
            schemaProyecto = ProyectoSchema()
            try:
                dictProyecto = schemaProyecto.load(datos)
                dictProyecto.save()
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'error': err.messages},404
        return {'name': datos},404

class ProyectoID(Resource):

    def get(self):
        datos = request.get_json()
        if datos:
             proyecto = Proyecto.find_by_id(datos['id'])
             if proyecto:
                return proyecto.json(), 200
        return {'name': f"No se encontró ningún proyecto con el ID {datos['id']}"},400