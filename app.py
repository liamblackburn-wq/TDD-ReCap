import sqlite3
from flask import Flask, render_template, request
from db import DatabaseService

app = Flask(__name__)

def get_db_service():
    connection = sqlite3.connect('duties.db', check_same_thread=False)
    return DatabaseService(connection)

@app.route("/", methods=["GET", "POST"])
def home():
    duty_list = [f"Duty {i}" for i in range(1, 14)]
    added_duties = []

    if request.method == "POST":
        if 'duties' not in request.form:
            return "Bad Request", 400

        selected_duties = request.form.getlist("duties")
        selected_ids = [int(name.split(" ")[1]) for name in selected_duties]

        service = get_db_service()
        added_duties = service.get_duty_descriptions(selected_ids)

    return render_template('index.html', duties=duty_list, added_duties=added_duties)
