from flask import request, jsonify, abort
from API.endpoints_methods import save_data, load_data, app
from Model.classes import Place
from Persistence.data_manager import data_manager
import json

places = {}

@app.route("/places", methods=["POST"])
def create_place():
    data = request.get_json()
    if not data or "name" not in data or "location" not in data:
        abort(400, description="Missing required fields: name, location")
    entity: Place = data_manager.create("Place", **data)
    data['id'] = entity.id
    save_data(data, "Persistence/places.json")
    # Respond with the newly created place
    return jsonify({'id': entity.id}), 201

@app.route("/places", methods=["GET"])
def get_places():
    all_places = data_manager.get_by_class("Place")
    if all_places is None:
        abort(404, description="No places found")
    return jsonify(load_data("Persistence/places.json"))

@app.route("/places/<place_id>", methods=["GET"])
def get_place_by_id(place_id):
    all_places = load_data("Persistence/places.json")
    for place in all_places:
        if place["id"] == place_id:
            return place
    return None

@app.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    all_places = load_data("Persistence/places.json")
    for place in all_places:
        if place["id"] == place_id:
            data = request.get_json()
            place["name"] = data["name"]
            place["location"] = data["location"]
            with open("Persistence/places.json", 'w') as f:
                json.dump(all_places, f)
            return jsonify(place)
    abort(404, description="Place not found")
    
@app.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    all_places = load_data("Persistence/places.json")
    for place in all_places:
        if place["id"] == place_id:
            all_places.remove(place)
            with open("Persistence/places.json", 'w') as f:
                json.dump(all_places, f)
            return jsonify(place)
    abort(404, description="Place not found")


