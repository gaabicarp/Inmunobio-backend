from flask import jsonify

class CommonService():
    
    def updateAtributes(object,atribute,keyExclude = ""):
        for key,value in atribute.items():
            print(key,value)
            if keyExclude != key and hasattr(object, key) :
                setattr(object, key, value)
        #object.save()

    def jsonMany(datos,schema):
        return jsonify(schema().dump(datos,many=True))
    
    def json(datos,schema):
        return schema().dump(datos)