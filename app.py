import sqlite3
from flask import Flask, render_template, request
from db import DatabaseService

app = Flask(__name__)

connection = sqlite3.connect('duties.db', check_same_thread=False)
db_service = DatabaseService(connection)

@app.route("/", methods=["GET", "POST"])
def home():
    duty_list = [f"Duty {i}" for i in range(1, 14)]
    added_duties = []

    if request.method == "POST":
        selected_duties = request.form.getlist("duties")
        selected_ids = [int(name.split(" ")[1]) for name in selected_duties]

        added_duties = db_service.get_duty_descriptions(selected_ids)

    return render_template('index.html', duties=duty_list, added_duties=added_duties)
