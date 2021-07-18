from werkzeug.security import safe_str_cmp
from servicios.usuarioService import UsuarioService
from werkzeug.security import check_password_hash

#TO-DO: probar authenticate con email
def authenticate(username, password):
    print("dasd1")
    user = UsuarioService.find_by_email(username)
    if user and check_password_hash(user.password, password):
        return user

def identity(payload):
    print(f"payload: {payload}")
    user_id = payload['identity']
    print(f"user_id: {user_id}")
    return UsuarioService.find_by_id(user_id)