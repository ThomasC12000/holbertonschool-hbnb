from flask import Flask
from flask import jsonify
from flask import request, abort
from Persistence.data_manager import data_manager
from Model.classes import Amenity
import json
import os

amenities = {}

app = Flask(__name__)

@app.route("/amenities", methods=["POST"])
def create_amenity():
    data = request.get_json()
    if not data or "name" not in data:
        abort(400, description="Missing required field: name")
    if not isinstance(data["name"], str):
        abort(400, description="Invalid name format")
    if amenity_exists(data["name"]):
        abort(409, description="An amenity with this name already exists")

    entity: Amenity = data_manager.create("Amenity", **data)
    data['id'] = entity.id
    save_data(data)
    # Respond with the newly created amenity
    return jsonify({'id': entity.id}), 201