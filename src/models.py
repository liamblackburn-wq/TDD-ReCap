import os
import uuid

from peewee import BooleanField, CharField, ForeignKeyField, TextField, UUIDField

from src.db import BaseModel


class Coin(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(unique=True)

    @property
    def status(self):
        links = list(self.assigned_duties)
        if not links:
            return "IN_PROGRESS"

        all_duties_done = all(link.is_complete for link in links)
        return "COMPLETED" if all_duties_done else "IN_PROGRESS"

    class Meta:
        if os.environ.get("TESTING") == "True":
            schema = "coins_test"
            table_name = "tdd_endgame_test_coins"
        else:
            schema = "coins"
            table_name = "tdd_endgame_coins"

    def validate(self):
        if any(char.isdigit() for char in self.name):
            raise ValueError("Coin names cannot contain numbers.")

    def __eq__(self, other):
        if not isinstance(other, Coin):
            return False
        return self.name == other.name


class Duty(BaseModel):
    id = UUIDField(primary_key=True)
    name = CharField(unique=True)
    description = TextField()

    class Meta:
        if os.environ.get("TESTING") == "True":
            schema = "coins_test"
            table_name = "tdd_safari_test_duties"
        else:
            schema = "coins"
            table_name = "tdd_safari_duties"

    def validate(self):
        if not self.name.startswith("Duty ") or not self.name[5:].isdigit():
            raise ValueError("Duty name must start with 'Duty' followed by a number.")

    def __eq__(self, other):
        if not isinstance(other, Duty):
            return False
        return self.name == other.name and self.description == other.description


class CoinsDutiesJunction(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    coin = ForeignKeyField(Coin, backref="assigned_duties", on_delete="CASCADE")
    duty = ForeignKeyField(Duty, backref="assigned_coins", on_delete="CASCADE")
    is_complete = BooleanField(default=False)

    class Meta:
        if os.environ.get("TESTING") == "True":
            schema = "coins_test"
            table_name = "tdd_endgame_test_junction"
        else:
            schema = "coins"
            table_name = "tdd_endgame_junction"

        indexes = ((("coin", "duty"), True),)
