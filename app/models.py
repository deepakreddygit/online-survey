

from peewee import Model, CharField, TextField, ForeignKeyField, DateTimeField
from app import db
from flask_login import UserMixin
import datetime
from datetime import datetime


class BaseModel(Model):
    class Meta:
        database = db

class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

class Survey(BaseModel):
    title = CharField()
    description = TextField(null=True)
    link = CharField(unique=True)  # Unique link for surveys
    user = ForeignKeyField(User, backref='surveys')

class Response(BaseModel):
    content = TextField()
    timestamp = DateTimeField(default=datetime.now)
    survey = ForeignKeyField(Survey, backref="responses")
