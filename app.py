import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from db import DatabaseService

app = Flask(__name__)


def get_db_service():
    connection = sqlite3.connect('duties.db', check_same_thread=False)
    return DatabaseService(connection)


@app.route("/", methods=["GET", "POST"])
def home():
    duty_list = [f"Duty {i}" for i in range(1, 14)]
    updated_duty_list = []
    service = get_db_service()

    if request.method == "POST":
        if 'duties' not in request.form:
            return "Bad Request", 400

        selected_duties = request.form.getlist("duties")
        selected_ids = [int(name.split(" ")[1]) for name in selected_duties]
        service.save_duties(selected_ids)

    added_duties = service.get_saved_duties()
    for duty in added_duties:
        updated_duty_list.append(duty["Duty"])

    available_duties = [duty for duty in duty_list if duty not in updated_duty_list]
    return render_template('index.html', duties=available_duties, added_duties=added_duties)


@app.route("/remove/<duty_id>", methods=["GET", "POST"])
def remove_duty(duty_id):
    service = get_db_service()
    service.remove_saved_duty(duty_id)
    return redirect(url_for('home'))

@app.route("/clear-duties", methods=["GET", "POST"])
def clear_duties():
    service = get_db_service()
    service.clear_saved_duties()
    return redirect(url_for('home'))
