import uuid
from flask import Flask, render_template, request, jsonify
from peewee import IntegrityError

from src.models import Duty, CoinsDutiesJunction, Coin
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

    all_duties = Duty.select()

    return render_template("index.html", added_duties=all_duties)


@app.route("/coins", methods=["GET", "POST"])
def coins_table_reqs():
    if request.method == 'POST':
        try:
            payload = request.get_json()

            coin_id = payload.get("id")
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
            {"id": coin.id,
             "name": coin.name,
             "status": coin.status
             }
            for coin in all_coins]

        return jsonify(coin_list)

@app.route('/coins/<uuid:coin_id>', methods=['DELETE'])
def delete_coin(coin_id):
    try:
        delete_query = Coin.delete().where(Coin.id == coin_id)
        deleted_coin = delete_query.execute()

        if deleted_coin == 0:
            return jsonify({"error": "Coin does not exist"}), 404
        else:
            return jsonify({'message': 'Coin deleted successfully'}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/coins/<uuid:coin_id>', methods=['PUT'])
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

        updated_coin = {'id': coin.id, 'name': coin.name, 'status': coin.status}

        return jsonify(updated_coin), 200

    except ValueError as val_err:
        return jsonify({"error": str(val_err)}), 400

    except IntegrityError:
        return jsonify({"error": "Coin already exists"}), 409

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/duties', methods=['GET', 'POST'])
def duties_table_reqs():
    if request.method == 'POST':
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
                "description": duty.description
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
            {
                "id": duty.id, "name": duty.name, "description": duty.description
            }
            for duty in all_duties
        ]

        return jsonify(duty_list), 200


@app.route('/duties/<uuid:duty_id>', methods=['DELETE'])
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


@app.route('/coin-duties', methods=['POST'])
def coin_duties_table_reqs():
    try:
        payload = request.get_json()
        coin_id = payload.get("coin_id")
        duty_id = payload.get("duty_id")
        CoinsDutiesJunction.create(coin=coin_id, duty=duty_id)

        new_association = {
            "coin_id": coin_id,
            "duty_id": duty_id
        }

        return jsonify(new_association), 201

    except IntegrityError:
        return jsonify({"error": "placeholder"}), 409

