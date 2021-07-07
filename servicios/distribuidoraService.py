from models.mongo.distribuidora import Distribuidora
from schemas.distribuidoraSchema import DistribuidoraSchema,ModificarDistribuidora,NuevaDistribuidoraSchema,IdDistribuidoraSchema
from servicios.commonService import CommonService
from exceptions.exception import ErrorDistribuidoraInexistente

class DistribuidoraService():
    @classmethod
    def altaDistribuidora(cls,datos):
            nuevaDistribuidora = NuevaDistribuidoraSchema().load(datos)
            cls.validacionDistribuidora(datos)
            nuevaDistribuidora.save()

    def validacionDistribuidora(datos):
        #debe validar algo la distribuidora?
        pass

    @classmethod    
    def find_by_id(cls,id):
        distribuidora =  Distribuidora.objects(id_distribuidora = id).first()
        if(not distribuidora):
            raise ErrorDistribuidoraInexistente()
        return distribuidora  
           
    @classmethod
    def bajaDistribuidora(cls,id_distribuidora):
            #valida si existe producto activo con esta id?
            distribuidora = cls.find_by_id(id_distribuidora)
            distribuidora.delete()

    @classmethod
    def obtenerDistribuidoras(cls):
        return CommonService.jsonMany(Distribuidora.objects().all(),DistribuidoraSchema)

    @classmethod
    def modificarDistribuidora(cls,datos):
            ModificarDistribuidora().load(datos)
            distribuidora = cls.find_by_id(datos['id_distribuidora'])
            CommonService.updateAtributes(distribuidora,datos,'id_distribuidora')
            distribuidora.save()
       
    @classmethod
    def obtenerNombreDistribuidora(cls,id):
        return cls.find_by_id(id).nombre