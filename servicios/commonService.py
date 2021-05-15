from flask import jsonify

class CommonService():
    
    def updateAtributes(object,atribute):
        for key,value in atribute.items():
                if hasattr(object, key) :
                    setattr(object, key, value)
        object.save()

    def jsonMany(datos,schema):
        return jsonify(schema().dump(datos,many=True))
    
    def json(datos,schema):
        return schema().dump(datos)