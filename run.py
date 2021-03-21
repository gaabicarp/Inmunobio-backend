from app import app
from db import db
from flask_mongoalchemy import MongoAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db.init_app(app)
dbMongo.init_app(app)
Migrate(app,db, compare_type=True)

@app.before_first_request
def create_tables():
    db.create_all()