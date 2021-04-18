from models.mongo.contenedor import Contenedor, ContenedorSchema, ContenedorNuevoSchema, ContenedorProyectoSchema, ContenedorParentSchema

class ContenedorService:

    @classmethod
    def find_by_id(cls, id):
        return Contenedor.objects.filter(id_contenedor=id).first()

    @classmethod
    def find_all(cls):
        return  ContenedorSchema().dump(Contenedor.objects.all(), many=True)
    
    @classmethod
    def find_all_by_id_proyecto(cls, id):
        return  ContenedorSchema().dump(Contenedor.objects.filter(id_proyecto=id).all(), many=True)

    @classmethod
    def nuevoContenedor(cls, datos):
        contenedor = ContenedorNuevoSchema().load(datos)
        contenedor.save()
    
    @classmethod
    def asignarProyectoAlContenedor(cls, datos):
        contenedor = ContenedorProyectoSchema().load(datos)
        Contenedor.objects(id_contenedor = contenedor.id_contenedor).update(id_proyecto= contenedor.id_proyecto)

    @classmethod
    def subContenedoresDelContenedor(cls, datos):
        contenedorPrincipal = ContenedorPrincipalSchema().load(datos)
        return ContenedorSchema().dump(Contenedor.objects(parent = contenedorPrincipal.id_contenedor).all(), many=True)
    
    @classmethod
    def asignarParents(cls, datos):
        #Falta corregir el map
        contenedores = datos.map(dato, ContenedorParentSchema().load(datos))
        contenedores.forEach(contenedor = Contenedor.objects(id_contenedor = contenedor.id_contenedor).update(parent = contenedor.parent))