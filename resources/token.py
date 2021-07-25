from functools import wraps
from flask.globals import request
import jwt
from servicios.usuarioService import UsuarioService

class TokenDeAcceso():

    SUPERUSUARIO = "Superusuario"
    DIR_CENTRO = "Director de centro"
    JEF_GRUP = "Jefe de grupo"
    BIO = "Director de proyecto / bioterio"
    TEC = "Técnico"

    def token_nivel_de_acceso(permisoUsuario):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                token = None
                if 'Authorization' in request.headers:
                    token = request.headers['Authorization']
                else:
                    return {'Error': 'Es necesario enviar un token.'}, 400
                from app import app
                try:
                    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                except Exception as err:
                    return {"Error": f"Token incorrecto. Mensaje del eror: {str(err)}"}, 400
                except jwt.ExpiredSignatureError:
                    return {"Error": f"Token vencido."}, 400
                permisosUsuario = UsuarioService.find_by_email(data['email']).permisos
                for permiso in permisosUsuario:
                    if permisoUsuario in permiso.descripcion:
                        return f(*args, **kwargs)
                return {"Error": f"El usuario {data['email']} no tiene permisos suficientes para realizar esta petición."}, 400
            return decorated_function
        return decorator