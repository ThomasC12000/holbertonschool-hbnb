from flask import Flask
from flask import jsonify
from flask import request, abort
from Persistence.data_manager import data_manager
from Model.classes import User
from API.endpoints_methods import save_data, email_exists, load_data, app
import json

users = {}

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "email" not in data or "first_name" not in data or "last_name" not in data:
        abort(400, description="Missing required fields: email, first_name, last_name, password")
    if not isinstance(data["email"], str) or "@" not in data["email"]:
        abort(400, description="Invalid email format")
    if email_exists(data["email"]):
        abort(409, description="A user with this email already exists")

    entity: User = data_manager.create("User", **data)
    data['id'] = entity.id
    save_data(data, "Persistence/users.json")
    # Respond with the newly created user
    return jsonify({'id': entity.id}), 201  # HTTP status 201 for Created

@app.route("/users", methods=["GET"])
def get_users():
    all_users = data_manager.get_by_class("User")
    if all_users is None:
        abort(404, description="No users found")
    return jsonify(load_data("Persistence/users.json"))

@app.route("/users/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    all_users = load_data("Persistence/users.json")
    for user in all_users:
        if user["id"] == user_id:
            return user
    return None

@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    all_users = load_data("Persistence/users.json")
    for user in all_users:
        if user["id"] == user_id:
            data = request.get_json()
            user["email"] = data["email"]
            user["first_name"] = data["first_name"]
            user["last_name"] = data["last_name"]
            with open("Persistence/users.json", 'w') as f:
                json.dump(all_users, f)
            return jsonify(user)
    abort(404, description="User not found")

@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    all_users = load_data("Persistence/users.json")
    for user in all_users:
        if user["id"] == user_id:
            all_users.remove(user)
            with open("Persistence/users.json", 'w') as f:
                json.dump(all_users, f)
            return jsonify(user)
    return None
