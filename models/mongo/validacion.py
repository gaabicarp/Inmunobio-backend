from marshmallow import validate

class Validacion():

    not_empty_string = validate.Length(min=1, error="El campo no puede estar vacío.")
    not_empty_int = validate.Range(min=1, error="El campo tiene que ser mayor a 0.")
    not_empty_list = validate.Length(min=1, error="La lista no puede estar vacía.")
