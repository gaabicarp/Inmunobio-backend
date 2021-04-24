from db import dbMongo
import json
from models.mongo.grupoDeTrabajo import jefeDeGrupoSchema,ModificarGrupoDeTrabajoSchema,GrupoDeTrabajoSchema,GrupoDeTrabajo,NuevoGrupoDeTrabajoSchema,BorrarGrupoDeTrabajoSchema
from marshmallow import Schema, ValidationError
from flask import jsonify, request
from servicios.usuarioService import UsuarioService

class GrupoDeTrabajoService:
    def find_by_id(id):
        return GrupoDeTrabajo.objects.filter(id_grupoDeTrabajo=id).first()

    def find_by_nombre(_nombre):
        return GrupoDeTrabajo.objects(nombre = _nombre).first()

    @classmethod
    def modificarMiembrosGrupo(cls,datos):
        try:
            ModificarGrupoDeTrabajoSchema().load(datos)
            grupoAModificar = cls.find_by_id(datos['id_grupoDeTrabajo'])
            if(grupoAModificar): 
                if (cls.validarMiembros(datos['integrantes'])) :
                    grupoAModificar.update(integrantes=datos['integrantes'])
                    return {'Status':'ok'},200  
                return {'error':'Usuario/s miembros invalidos'},404
            return {'error':'El grupo no existe '},404
        except ValidationError as err:
            return {'error': err.messages},404

    @classmethod
    def modificarJefeGrupo(cls,datos):
        try:
            jefeDeGrupoSchema().load(datos)
            grupoAModificar = cls.find_by_id(datos['id_grupoDeTrabajo'])
            if(grupoAModificar):
                if(cls.validarMiembros([datos['jefeDeGrupo']])):
                    grupoAModificar.update(jefeDeGrupo=datos['jefeDeGrupo'])
                    return {'Status':'ok'},200  
                return {'error':'Jefe de grupo inexistente'},404
            return {'error':'Grupo inexistente'},404
        except ValidationError as err:
            return {'error': err.messages},404

    def nuevoGrupo(datos):
        try:
            grupoCreado = NuevoGrupoDeTrabajoSchema().load(datos)
            if(validarMiembros([grupoCreado.jefeDeGrupo])):
                grupoCreado.save()
                return {'Status':'ok'},200  
            return {'error':'No existe usuario con id '+str(datos['jefeDeGrupo'])},404
        except ValidationError as err:
            return {'error': err.messages},404

    @classmethod
    def removerGrupo(cls,datos):
        #falta ver que pasa con los roles de un jefe cuando se borra el grupo 
        #falta ver que no sea grupo general
        try:
            BorrarGrupoDeTrabajoSchema().load(datos)
            grupoABorrar = GrupoDeTrabajoService.find_by_id(datos['id_grupoDeTrabajo'])
            if(grupoABorrar):
                if(cls.validarDelete(grupoABorrar)):
                    grupoABorrar.delete()
                    return {'Status':'ok'},200
                return {'Status': 'El grupo no puede ser dado de baja por contener stock activo'}
            return {'Status': 'No existe el grupo'}
        except ValidationError as err:
            return {'error': err.messages},404

    def obtenerGrupoPorId(datos):
        try:
            BorrarGrupoDeTrabajoSchema().load(datos)
            grupoConsulta= GrupoDeTrabajoService.find_by_id(datos['id_grupoDeTrabajo'])
            if (grupoConsulta):
                return GrupoDeTrabajoService.json(grupoConsulta)
            return  {'error':'El grupo de trabajo no existe'},404    
        except ValidationError as err:
            return {'error': err.messages},404

    def validarDelete(grupo):
        return len(grupo.stock) == 0

    def validarMiembros(integrantes):
        '''recibe una listacon id de usuarios devuelve true si todos existen o false en caso contrario'''
        for idIntegrante in integrantes:
            if(not UsuarioService.find_by_id(idIntegrante)):
                print("id"+ str(idIntegrante) + "no existe")
                return False
        print("se encontraron todos los usuarios")
        return True

    def json(datos):
        return GrupoDeTrabajoSchema().dump(datos)

    def jsonMany(datos):
        return jsonify(GrupoDeTrabajoSchema().dump(datos,many=True))

    def obtenerTodosLosGrupos():
        return GrupoDeTrabajo.objects.all()