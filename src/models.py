from src.db import BaseModel
from peewee import *

class Duty(BaseModel):
    id = UUIDField(primary_key=True)
    name = CharField(unique=True)
    description = TextField()

    class Meta:
        table_name = 'tdd-safari-duties'
        schema = 'coins'
