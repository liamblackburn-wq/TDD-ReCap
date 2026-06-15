import os
from src.db import BaseModel
from peewee import *

class Duty(BaseModel):
    id = UUIDField(primary_key=True)
    name = CharField(unique=True)
    description = TextField()

    class Meta:

        if os.environ.get('TESTING') == 'True':
            schema = 'coins_test'
            table_name = 'tdd_safari_test_duties'
        else:
            schema = 'coins'
            table_name = 'tdd_safari_duties'

    def validate(self):
        if not self.name.startswith("Duty ") or not self.name[5:].isdigit():
            raise ValueError("Duty name must start with 'Duty' followed by a number.")

    def __eq__(self, other):
        if not isinstance(other, Duty):
            return False
        return self.name == other.name and self.description == other.description