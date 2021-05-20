from flask import jsonify

class CommonService():
    
    def updateAtributes(object,atribute,keyExclude = ""):
        for key,value in atribute.items():
            print(key,value)
            if keyExclude != key and hasattr(object, key) :
                setattr(object, key, value)
        #object.save()

    def comparar(objeto,otroObjeto,atributos):
        for att in atributos:
            if (getattr(objeto,att) != getattr(otroObjeto,att)): return False
        return True

    def jsonMany(datos,schema):
        return jsonify(schema().dump(datos,many=True))
    
    def json(datos,schema):
        return schema().dump(datos)