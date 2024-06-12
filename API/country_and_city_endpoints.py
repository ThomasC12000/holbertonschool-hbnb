from flask import request, jsonify, abort
from API.endpoints_methods import save_data, load_data, app
from Model.classes import City
from Model.base_class import BaseClass
from Persistence.data_manager import data_manager
import json


@app.route("/cities", methods=["POST"])
def create_city():
    data = request.get_json()
    if not data or "name" not in data or "country" not in data:
        abort(400, description="Missing required fields: name, country")
    entity = data_manager.create("City", **data)
    data['id'] = entity.id
    save_data(data, "Persistence/cities.json")
    # Respond with the newly created city
    return jsonify({'id': entity.id}), 201

@app.route("/cities", methods=["GET"])
def get_cities():
    all_cities = data_manager.get_by_class("City")
    if all_cities is None:
        abort(404, description="No cities found")
    return jsonify(load_data("Persistence/cities.json"))

@app.route("/cities/<city_id>", methods=["GET"])
def get_city_by_id(city_id):
    all_cities = load_data("Persistence/cities.json")
    for city in all_cities:
        if city["id"] == city_id:
            return city
    return None

@app.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    all_cities = load_data("Persistence/cities.json")
    for city in all_cities:
        if city["id"] == city_id:
            data = request.get_json()
            city["name"] = data["name"]
            city["country"] = data["country"]
        with open("Persistence/cities.json", 'w') as f:
            json.dump(all_cities, f)
        return jsonify(city)
    abort(404, description="City not found")

@app.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    all_cities = load_data("Persistence/cities.json")
    for city in all_cities:
        if city["id"] == city_id:
            all_cities.remove(city)
        with open("Persistence/cities.json", 'w') as f:
            json.dump(all_cities, f)
        return jsonify(city)
    abort(404, description="City not found")

@app.route("/countries", methods=["GET"])
def get_countries():
    all_countries = data_manager.get_by_class("Country")
    if all_countries is None:
        abort(404, description="No countries found")
    return jsonify(load_data("Persistence/countries.json"))

@app.route("/countries/<country_code>", methods=["GET"])
def get_country_by_code(country_code):
    all_countries = load_data("Persistence/countries.json")
    for country in all_countries:
        if country["code"] == country_code:
            return country
    return None

@app.route("/countries/<country_code>/cities", methods=["GET"])
def get_cities_by_country(country_code):
    all_cities = load_data("Persistence/cities.json")
    cities_in_country = [city for city in all_cities if city["country"] == country_code]
    if not cities_in_country:
        abort(404, description="No cities found in this country")
    return jsonify(cities_in_country)
