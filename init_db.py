import os
from dotenv import load_dotenv

load_dotenv()

from src.db import db  # noqa: E402
from src.models import Duty, Coin, CoinsDutiesJunction, RequestLog, User  # noqa: E402

apprentice_raw_password = os.getenv("APPRENTICE_PASSWORD")
admin_raw_password = os.getenv("ADMIN_PASSWORD")


def initialise_database():
    print("Connecting to PostgreSQL")
    db.connect(reuse_if_open=True)

    print("Creating table")
    db.create_tables([Duty, Coin, CoinsDutiesJunction, RequestLog, User], safe=True)

    if User.get_or_none(User.username == os.getenv("APPRENTICE_USERNAME")) is None:
        User.create_user(
            username=os.getenv("APPRENTICE_USERNAME"),
            password=apprentice_raw_password,
            role=os.getenv("APPRENTICE_ROLE"),
        )
        print("Apprentice user created! 🎉")
    else:
        print("Apprentice already exists, skipping creation.")

    if User.get_or_none(User.username == os.getenv("ADMIN_USERNAME")) is None:
        User.create_user(
            username=os.getenv("ADMIN_USERNAME"),
            password=admin_raw_password,
            role=os.getenv("ADMIN_ROLE"),
        )
        print("Admin user created! 🎉")
    else:
        print("Admin already exists, skipping creation.")

    db.close()
    print("Database initialisation complete! 🚀")


if __name__ == "__main__":
    initialise_database()
