from flask import Flask
from flask import jsonify
from flask import request, abort
from Persistence.data_manager import data_manager
from Model.users import Users
import json



users = {}

app = Flask(__name__)

users_manager = Users()

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "email" not in data or "first_name" not in data or "last_name" not in data:
        abort(400, description="Missing required fields: email, first_name, last_name")
    if not isinstance(data["email"], str) or "@" not in data["email"]:
        abort(400, description="Invalid email format")

    entity = data_manager.create("User", **data)
    # Respond with the newly created user
    return jsonify({'id': user_id}), 201  # HTTP status 201 for Created


@app.route("/users", methods=["GET"])
def get_users():
    all_users = users_manager.get_all_users()
    if not all_users:
        abort(404, description="No users found")