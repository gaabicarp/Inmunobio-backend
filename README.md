
# Pasos para levantar el entorno:

-Requerimientos: tener python 3.x instalado.
-
## 1-Clonar el proyecto
## 2-Crear environment dentro de la carpeta raíz:

$python3 -m venv env

## 3-Entrar al entorno e instalar librerías:
$source /path/to/env/bin/activate
(El prompt de la consola debe cambiar a (env)
$pip install wheel 
$pip install -r requirements.txt

## 4-Levantar la app dentro de la carpeta raíz:
$python app.py

Posibles errores solucionables con algunos de estos comandos:
$apt-get install libmysqlclient-dev python-dev (Fuera del entorno)


 
