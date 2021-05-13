
class CommonService():
    
    def updateAtributes(object,atribute):
        for key,value in atribute.items():
                if hasattr(object, key) :
                    setattr(object, key, value)
        object.save()