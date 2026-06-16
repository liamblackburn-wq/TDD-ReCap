import os
from src.db import BaseModel
from peewee import *

class Coin(BaseModel):
    id = UUIDField(primary_key=True)
    name = CharField(unique=True)

    class Meta:
        if os.environ.get('TESTING') == 'True':
            schema = 'coins_test'
            table_name = 'tdd_endgame_test_coins'
        else:
            schema = 'coins'
            table_name = 'tdd_endgame_coins'

    def validate(self):
        if self.name.isdigit():
            raise ValueError("Coin names can not contain numbers.")

    def __eq__(self, other):
        if not isinstance(other, Coin):
            return False
        return self.name == other.name


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

class CoinsDutiesJunction(BaseModel):
    coin = ForeignKeyField(Coin, backref="assigned_duties")
    duty = ForeignKeyField(Duty, backref="assigned_coins")

    class Meta:
        if os.environ.get('TESTING') == 'True':
            schema = 'coins_test'
            table_name = 'tdd_endgame_test_junction'
        else:
            schema = 'coins'
            table_name = 'tdd_endgame_junction'