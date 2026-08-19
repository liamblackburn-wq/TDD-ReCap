import os
import uuid
from functools import wraps
import html

from flask import Flask, request, jsonify, render_template, abort, redirect
from flask_login import (
    LoginManager,
    login_user,
    current_user,
    logout_user,
    login_required,
)
from peewee import IntegrityError, DatabaseError

from src.models import Duty, CoinsDutiesJunction, Coin, RequestLog, User
from src.db import db

# TODO 2: create logout functionality
# TODO 3: Fill in e2e test
# TODO 4: coins_duties_model unit tests

app = Flask(__name__)
app.config['DEBUG'] = False
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)

        if current_user.role != "admin":
            abort(403)

        return f(*args, **kwargs)

    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get_or_none(User.id == uuid.UUID(user_id))
    except (ValueError, TypeError):
        return None


@app.before_request
def _db_connect():
    if request.endpoint == "static":
        return

    db.connect(reuse_if_open=True)


@app.after_request
def request_logger(response):
    ignored_prefixes = ("/.well-known/", "/static", "/favicon.ico")

    if request.path.startswith(ignored_prefixes):
        return response

    path = request.path
    status_code = response.status_code
    request_method = request.method

    RequestLog.create(
        endpoint=path,
        status_code=status_code,
        request_method=request_method,
    )

    response.headers["Server"] = "Protected-Server"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self';"
    )

    return response


@app.teardown_request
def _db_close(exc):
    if request.endpoint == "static":
        return

    if not db.is_closed():
        db.close()


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    user = User.get_or_none(User.username == username)

    if user and user.check_password(password):
        login_user(user)
        return jsonify({"message": "Logged in successfully", "role": user.role}), 200

    return jsonify({"message": "Invalid username or password"}), 401


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Page not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "An internal server error occurred"}), 500


@app.route("/api/logout", methods=["POST"])
def api_logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


@app.route("/api/logs", methods=["GET"])
@admin_required
def get_logs():
    logs = RequestLog.select().order_by(RequestLog.timestamp.desc()).limit(100)

    log_list = [
        {
            "id": log.id,
            "path": log.endpoint,
            "request_method": log.request_method,
            "status_code": log.status_code,
            "timestamp": log.timestamp.isoformat(),
        }
        for log in logs
    ]

    return jsonify(log_list), 200


@app.route("/logs")
@admin_required
def render_logs_page():
    return render_template("logger.html")


@app.route("/", methods=["GET"])
def home():
    if current_user.is_authenticated:
        return redirect("/apprenticeduties")
    return render_template("login.html")


@app.route("/api/role", methods=["GET"])
def get_role():
    if current_user.is_authenticated:
        return jsonify({"role": current_user.role}), 200
    return jsonify({"role": "guest"}), 200


@app.route("/apprenticeduties", methods=["GET"])
def render_apprentice_duties_page():
    return render_template("index.html")


@app.route("/coins", methods=["GET"])
def get_coins():
    all_coins = Coin.select()

    coin_list = [
        {"id": coin.id, "name": coin.name, "status": coin.status} for coin in all_coins
    ]

    return jsonify(coin_list)


@app.route("/coins", methods=["POST"])
@admin_required
def coins_table_reqs():
    try:
        payload = request.get_json() or {}
        coin_id = payload.get("id") or str(uuid.uuid4())
        coin_name = html.escape((payload.get("name") or "").strip())
        coin = Coin(id=coin_id, name=coin_name)
        coin.validate()
        coin.save(force_insert=True)
        new_coin = {"id": coin.id, "name": coin.name, "status": coin.status}
        return jsonify(new_coin), 201
    except ValueError as val_err:
        return jsonify({"error": str(val_err)}), 400
    except IntegrityError:
        return jsonify({"error": "Coin already exists"}), 409


@app.route("/coins/<uuid:coin_id>", methods=["DELETE"])
@admin_required
def delete_coin(coin_id):
    try:
        delete_query = Coin.delete().where(Coin.id == coin_id)
        deleted_coin = delete_query.execute()

        if deleted_coin == 0:
            return jsonify({"error": "Coin does not exist"}), 404
        else:
            return jsonify({"message": "Coin deleted successfully"}), 200
    except DatabaseError:
        return jsonify({"error": "An internal server error occurred"}), 500


@app.route("/coins/<uuid:coin_id>", methods=["PUT"])
@login_required
def update_coin(coin_id):
    try:
        coin = Coin.get_or_none(Coin.id == coin_id)

        if coin is None:
            return jsonify({"error": "Coin does not exist"}), 404

        payload = request.get_json() or {}
        new_coin_name = html.escape((payload.get("name") or "").strip())

        coin.name = new_coin_name

        coin.validate()

        coin.save()

        updated_coin = {"name": coin.name, "status": coin.status}

        return jsonify(updated_coin), 200

    except ValueError as val_err:
        return jsonify({"error": str(val_err)}), 400

    except IntegrityError:
        return jsonify({"error": "Coin already exists"}), 409

    except DatabaseError:
        return jsonify({"error": "An internal server error occurred"}), 500


@app.route("/duties", methods=["GET"])
def get_duties():
    all_duties = Duty.select()

    duty_list = [
        {"id": duty.id, "name": duty.name, "description": duty.description}
        for duty in all_duties
    ]
    return jsonify(duty_list), 200


@app.route("/duties", methods=["POST"])
@admin_required
def duties_table_reqs():
    try:
        payload = request.get_json() or {}
        duty_id = payload.get("id") or str(uuid.uuid4())
        duty_name = html.escape((payload.get("name") or "").strip())
        duty_description = html.escape((payload.get("description") or "").strip())
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


@app.route("/duties/<uuid:duty_id>", methods=["DELETE"])
@admin_required
def delete_duty(duty_id):
    try:
        delete_query = Duty.delete().where(Duty.id == duty_id)
        deleted_duty = delete_query.execute()
        if deleted_duty == 0:
            return jsonify({"error": "Duty does not exist"}), 404
        else:
            return jsonify({"message": "Duty deleted successfully"}), 200
    except DatabaseError:
        return jsonify({"error": "An internal server error occurred"}), 500


@app.route("/coin-duties", methods=["GET"])
def get_coins_duties():
    all_links = (
        CoinsDutiesJunction.select(CoinsDutiesJunction, Duty, Coin)
        .join(Duty)
        .switch(CoinsDutiesJunction)
        .join(Coin)
    )

    linked_list = [
        {
            "id": linked.id,
            "coin_id": linked.coin.id,
            "duty_id": linked.duty.id,
            "is_complete": linked.is_complete,
            "duty_name": linked.duty.name,
            "duty_description": linked.duty.description,
        }
        for linked in all_links
    ]
    return jsonify(linked_list), 200


@app.route("/coin-duties", methods=["POST"])
@admin_required
def coin_duties_table_reqs():
    try:
        payload = request.get_json() or {}
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


@app.route("/coin-duties/<uuid:link_id>", methods=["PUT"])
@login_required
def update_coin_duties(link_id):
    try:
        payload = request.get_json() or {}
        update_progress = payload.get("is_complete")
        linked_id = CoinsDutiesJunction.get_or_none(CoinsDutiesJunction.id == link_id)
        if linked_id is None:
            return jsonify({"error": "Link does not exist"}), 404
        linked_id.is_complete = update_progress
        linked_id.save()
        return jsonify({"id": linked_id.id, "is_complete": linked_id.is_complete}), 200
    except DatabaseError:
        return jsonify({"error": "An internal server error occurred"}), 500


@app.route("/coin-duties/<uuid:link_id>", methods=["DELETE"])
@admin_required
def delete_coin_duties(link_id):
    try:
        deleted_count = CoinsDutiesJunction.delete_by_id(link_id)
        if deleted_count == 0:
            return jsonify({"error": "Link does not exist"}), 404
        return jsonify({"message": "Duty unlinked successfully", "id": str(link_id)}), 200
    except DatabaseError:
        return jsonify({"error": "An internal server error occurred"}), 500


