from flask import Flask
from flask import jsonify
from flask import request, abort
from Persistence.data_manager import data_manager
from Model.classes import User
from API.endpoints_methods import save_data, email_exists, load_data
from typing import Dict

users = {}

app = Flask(__name__)

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
    save_data(data)
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
            save_data(all_users)
            return user
    return None

@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    all_users = load_data("Persistence/users.json")
    for user in all_users:
        if user["id"] == user_id:
            all_users.popitem(user)
            save_data(all_users)
            return user
    return None

# def save_data(data):
#     file_path = "Persistence/users.json"

#     # Read existing data if the file exists
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as f:
#             try:
#                 existing_data = json.load(f)
#             except json.JSONDecodeError:
#                 existing_data = []
#     else:
#         existing_data = []

#     # Add the new data to the existing data
#     if existing_data != data:
#         existing_data.append(data)

#     # Write the updated data to the file
#     with open(file_path, 'w') as f:
#         json.dump(existing_data, f)

# def email_exists(email):
#     file_path = "Persistence/users.json"
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as f:
#             try:
#                 existing_users = json.load(f)
#             except json.JSONDecodeError:
#                 existing_users = []

#         for user in existing_users:
#             if user.get("email") == email:
#                 return True
#     return False

# def load_data(filename=None):
#     try:
#         with open(filename, 'r') as f:
#             return json.load(f)
#     except:
#         return {}

app.run()
