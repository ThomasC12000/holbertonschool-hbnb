from flask import Flask
from flask import jsonify
from flask import request, abort
from Persistence.data_manager import data_manager
from Model.classes import Amenity
from API.endpoints_methods import save_data, amenity_exists, load_data, app
import json

amenities = {}

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
    save_data(data, "Persistence/amenities.json")
    # Respond with the newly created amenity
    return jsonify({'id': entity.id}), 201

@app.route("/amenities", methods=["GET"])
def get_amenities():
    all_amenities = data_manager.get_by_class("Amenity")
    if all_amenities is None:
        abort(404, description="No amenities found")
    return jsonify(load_data("Persistence/amenities.json"))

@app.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity_by_id(amenity_id):
    all_amenities = load_data("Persistence/amenities.json")
    for amenity in all_amenities:
        if amenity["id"] == amenity_id:
            return amenity
    return None

@app.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    all_amenities = load_data("Persistence/amenities.json")
    for amenity in all_amenities:
        if amenity["id"] == amenity_id:
            data = request.get_json()
            amenity["name"] = data["name"]
            with open("Persistence/amenities.json", 'w') as f:
                json.dump(all_amenities, f)
            return jsonify(amenity)
    abort(404, description="Amenity not found")

@app.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    all_amenities = load_data("Persistence/amenities.json")
    for amenity in all_amenities:
        if amenity["id"] == amenity_id:
            all_amenities.remove(amenity)
            with open("Persistence/amenities.json", 'w') as f:
                json.dump(all_amenities, f)
            return jsonify(amenity)
    abort(404, description="Amenity not found")