from werkzeug.security import safe_str_cmp
from models.usuario import Usuario


def authenticate(username, password):
    user = Usuario.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return Usuario.find_by_id(user_id)