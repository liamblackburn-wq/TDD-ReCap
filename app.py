import uuid
from flask import Flask, request, jsonify, render_template
from flask_login import LoginManager, current_user, login_user, logout_user
from peewee import IntegrityError

from src.user_auth import User
from src.models import Duty, CoinsDutiesJunction, Coin
from src.db import db
app = Flask(__name__)
app.secret_key = 'secret key'

login_manager = LoginManager()
login_manager.init_app(app)

mock_users = {
    "admin": {"role": "admin"},
    "user": {"role": "user"},
}

@login_manager.user_loader
def load_user(user_id):
    if user_id in mock_users:
        user_role = mock_users[user_id]["role"]
        return User(id=user_id, role=user_role)
    return None

@app.before_request
def _db_connect():
    if db.is_closed():
        db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "admin 123":
        user = User(id="admin", role="admin")
        login_user(user)
        return jsonify({"message": "Logged in successfully", "role": "admin"}), 200
    elif username == "user" and password == "user123":
        user = User(id="user", role="user")
        login_user(user)
        return jsonify({"message": "Logged in successfully", "role": "user"}), 200
    return jsonify({"message": "Invalid username or password"}), 401

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/coins", methods=["GET", "POST"])
def coins_table_reqs():
    if request.method == "POST":
        try:
            payload = request.get_json()

            coin_id = payload.get("id") or str(uuid.uuid4())
            coin_name = payload.get("name")

            coin = Coin(id=coin_id, name=coin_name)

            coin.validate()

            coin.save(force_insert=True)

            new_coin = {"id": coin.id, "name": coin.name, "status": coin.status}

            return jsonify(new_coin), 201

        except ValueError as val_err:
            return jsonify({"error": str(val_err)}), 400

        except IntegrityError:
            return jsonify({"error": "Coin already exists"}), 409

    else:
        all_coins = Coin.select()

        coin_list = [
            {"id": coin.id, "name": coin.name, "status": coin.status}
            for coin in all_coins
        ]

        return jsonify(coin_list)


@app.route("/coins/<uuid:coin_id>", methods=["DELETE"])
def delete_coin(coin_id):
    try:
        delete_query = Coin.delete().where(Coin.id == coin_id)
        deleted_coin = delete_query.execute()

        if deleted_coin == 0:
            return jsonify({"error": "Coin does not exist"}), 404
        else:
            return jsonify({"message": "Coin deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/coins/<uuid:coin_id>", methods=["PUT"])
def update_coin(coin_id):
    try:
        coin = Coin.get_or_none(Coin.id == coin_id)

        if coin is None:
            return jsonify({"error": "Coin does not exist"}), 404

        payload = request.get_json()
        new_coin_name = payload.get("name")

        coin.name = new_coin_name

        coin.validate()

        coin.save()

        updated_coin = {"name": coin.name, "status": coin.status}

        return jsonify(updated_coin), 200

    except ValueError as val_err:
        return jsonify({"error": str(val_err)}), 400

    except IntegrityError:
        return jsonify({"error": "Coin already exists"}), 409

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/duties", methods=["GET", "POST"])
def duties_table_reqs():
    if request.method == "POST":
        try:
            payload = request.get_json()

            duty_id = payload.get("id") or str(uuid.uuid4())
            duty_name = payload.get("name")
            duty_description = payload.get("description")

            duty = Duty(id=duty_id, name=duty_name, description=duty_description)

            duty.validate()

            duty.save(force_insert=True)

            new_duty = {
                "id": duty.id,
                "name": duty.name,
                "description": duty.description,
            }

            return jsonify(new_duty), 201

        except ValueError as val_err:
            print(val_err)
            return jsonify({"error": str(val_err)}), 400

        except IntegrityError:
            return jsonify({"error": "Duty already exists"}), 409

    else:
        all_duties = Duty.select()

        duty_list = [
            {"id": duty.id, "name": duty.name, "description": duty.description}
            for duty in all_duties
        ]

        return jsonify(duty_list), 200


@app.route("/duties/<uuid:duty_id>", methods=["DELETE"])
def delete_duty(duty_id):
    try:
        delete_query = Duty.delete().where(Duty.id == duty_id)
        deleted_duty = delete_query.execute()

        if deleted_duty == 0:
            return jsonify({"error": "Duty does not exist"}), 404
        else:
            return jsonify({"message": "Duty deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/coin-duties", methods=["GET", "POST"])
def coin_duties_table_reqs():
    if request.method == "POST":
        try:
            payload = request.get_json()
            coin_id = payload.get("coin_id")
            duty_id = payload.get("duty_id")

            coin = Coin.get_or_none(Coin.id == coin_id)
            duty = Duty.get_or_none(Duty.id == duty_id)

            if coin is None:
                return jsonify({"error": "Coin does not exist"}), 404
            if duty is None:
                return jsonify({"error": "Duty does not exist"}), 404

            new_link = CoinsDutiesJunction.create(coin=coin_id, duty=duty_id)

            new_association = {
                "id": new_link.id,
                "coin_id": coin_id,
                "duty_id": duty_id,
            }

            return jsonify(new_association), 201

        except IntegrityError:
            return jsonify({"error": "Duty is already assigned to coin"}), 409
    else:
        all_links = CoinsDutiesJunction.select()

        linked_list = [
            {"id": linked.id, "is_complete": linked.is_complete} for linked in all_links
        ]
        return jsonify(linked_list), 200


@app.route("/coin-duties/<uuid:link_id>", methods=["PUT"])
def update_coin_duties(link_id):
    try:
        payload = request.get_json()
        update_progress = payload.get("is_complete")

        linked_id = CoinsDutiesJunction.get_or_none(CoinsDutiesJunction.id == link_id)

        if linked_id is None:
            return jsonify({"error": "Link does not exist"}), 404

        linked_id.is_complete = update_progress

        linked_id.save()

        updated_link = {
            "id": linked_id.id,
            "is_complete": linked_id.is_complete,
        }
        return jsonify(updated_link), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
