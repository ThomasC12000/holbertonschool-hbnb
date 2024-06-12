from flask import Flask
from flask import jsonify
from flask import request, abort
from Persistence.data_manager import data_manager
from Model.classes import Place
from API.endpoints_methods import save_data, load_data, email_exists

places = {}

app = Flask(__name__)


@app.route("/places", methods=["POST"])
def create_place():
    data = request.get_json()
    if not data or "name" not in data or "city_id" not in data or "user_id" not in data:
        abort(400, description="Missing required fields: name, city_id, user_id")
    if not isinstance(data["name"], str) or not isinstance(data["city_id"], str) or\
    not isinstance(data["user_id"], str):
        abort(400, description="Invalid input format")
    if not data_manager.exists(data["city_id"], "City"):
        abort(404, description="City not found")
    if not data_manager.exists(data["user_id"], "User"):
        abort(404, description="User not found")

    entity = data_manager.create("Place", **data)
    data['id'] = entity.id
    save_data(data)
    # Respond with the newly created place
    
    return jsonify({'id': entity.id}), 201  # HTTP status 201 for Created

