from models.mongo.proyecto import Proyecto, ProyectoSchema
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
            schemaProyecto = ProyectoSchema()
            nuevoProyecto = schemaProyecto.load(datos)
            #nuevoProyecto = Proyecto()
            #nuevoProyecto.nombre = datos['nombre']
            #nuevoProyecto.descripcion = datos['descripcion']
            #nuevoProyecto.montoInicial = datos['montoInicial']

            nuevoProyecto.save()
            return {'Status':'ok'},200
        return {'name': datos},404

class ProyectoID(Resource):

    def get(self):
        datos = request.get_json()
        if datos:
             proyecto = Proyecto.find_by_id(datos['id'])
             if proyecto:
                return proyecto.json(), 200
        return {'name': f"No se encontró ningún proyecto con el ID {datos['id']}"},400