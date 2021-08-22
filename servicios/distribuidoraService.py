from models.mongo.distribuidora import Distribuidora
from schemas.distribuidoraSchema import ModificarDistribuidora,NuevaDistribuidoraSchema
from servicios.commonService import CommonService

class DistribuidoraService():
    @classmethod
    def altaDistribuidora(cls,datos):
            nuevaDistribuidora = NuevaDistribuidoraSchema().load(datos)
            nuevaDistribuidora.save()

    @classmethod    
    def find_by_id(cls,id):
        distribuidora =  Distribuidora.objects(id_distribuidora = id).first()
        if(not distribuidora):raise Exception(f"Distribuidora con id.{id} inexistente")
        return distribuidora  
           
    @classmethod
    def bajaDistribuidora(cls,id_distribuidora):
            distribuidora = cls.find_by_id(id_distribuidora)
            from servicios.productoService import ProductoService
            ProductoService.bajaStockExterno(id_distribuidora)
            distribuidora.delete()

    @classmethod
    def obtenerDistribuidoras(cls):
        return Distribuidora.objects().all()

    @classmethod
    def modificarDistribuidora(cls,datos):
            ModificarDistribuidora().load(datos)
            distribuidora = cls.find_by_id(datos['id_distribuidora'])
            CommonService.updateAtributes(distribuidora,datos,'id_distribuidora')
            distribuidora.save()
       
    @classmethod
    def obtenerNombreDistribuidora(cls,id):
        return cls.find_by_id(id).nombre