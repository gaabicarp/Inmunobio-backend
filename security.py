from werkzeug.security import safe_str_cmp
from servicios.usuarioService import UsuarioService
from werkzeug.security import check_password_hash

def authenticate(username, password):
    user = UsuarioService.find_by_email(username)
    if user and check_password_hash(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UsuarioService.find_by_id(user_id)