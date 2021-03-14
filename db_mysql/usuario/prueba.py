from flask import Flask
from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, Integer, String, Text, Float
from app import db

class Prueba(db.Model):
	__tablename__ = 'prueba'
	id = db.Column(db.Integer, primary_key=True)
	prueba = db.Column(db.String)

	def __init__(self, id, prueba):
		self.id = id
		self.prueba = prueba