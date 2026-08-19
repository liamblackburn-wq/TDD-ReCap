import os
import socket
from dotenv import load_dotenv
from peewee import PostgresqlDatabase, Model

load_dotenv()

raw_host = os.getenv("DATABASE_HOST")

try:
    db_host = socket.getaddrinfo(raw_host, None, socket.AF_INET)[0][4][0]
except socket.gaierror:
    db_host = raw_host

db = PostgresqlDatabase(
    os.getenv("DATABASE"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=db_host,
    port=25060,
)


class BaseModel(Model):
    class Meta:
        database = db
