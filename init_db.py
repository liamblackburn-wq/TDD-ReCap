from src.db import db
from src.models import Duty, Coin, CoinsDutiesJunction, RequestLog


def initialise_database():
    print("Connecting to PostgreSQL")
    db.connect(reuse_if_open=True)

    print("Creating table")
    db.create_tables([Duty, Coin, CoinsDutiesJunction, RequestLog], safe=True)

    db.close()
    print("Database initialisation complete! 🚀")


if __name__ == "__main__":
    initialise_database()
