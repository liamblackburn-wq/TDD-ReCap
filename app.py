from flask import Flask, render_template, request, jsonify
from peewee import IntegrityError

from src.models import Duty
from src.db import db

app = Flask(__name__)

@app.before_request
def _db_connect():
    if db.is_closed():
        db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route('/duties', methods=['GET', 'POST'])
def duties_table_reqs():
    if request.method == 'POST':
        try:
            payload = request.get_json()

            duty_id = payload.get("id")
            duty_name = payload.get("name")
            duty_description = payload.get("description")

            duty = Duty.create(id=duty_id, name=duty_name, description=duty_description)

            new_duty = {
                "id": duty.id,
                "name": duty.name,
                "description": duty.description
            }

            return jsonify(new_duty), 201

        except IntegrityError:
            return jsonify({"error": "Duty already exists"}), 409

    else:
        all_duties = Duty.select()

        duty_list = [
            {
                "id": duty.id, "name": duty.name, "description": duty.description
            }
            for duty in all_duties
        ]

        return jsonify(duty_list)
