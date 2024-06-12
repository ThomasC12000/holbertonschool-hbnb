from flask import Flask, request, jsonify, abort
from API.endpoints_methods import save_data, load_data


app = Flask(__name__)

# Mock data
countries = {"US": "United States", "CA": "Canada", "FR": "France"}
cities = {
    1: {"name": "New York", "country_code": "US"},
    2: {"name": "Los Angeles", "country_code": "US"},
    3: {"name": "Toronto", "country_code": "CA"},
}

# Function to get the next city ID
def get_next_city_id():
    return max(cities.keys()) + 1 if cities else 1

@app.route("/countries/<country_code>/cities", methods=["GET"])
def get_cities_by_country(country_code):
    country_code = country_code.upper()
    if country_code not in countries:
        abort(404, description="Country code not found")
    
    result = [city for city in cities.values() if city["country_code"] == country_code]
    return jsonify({"country_code": country_code, "cities": result})

@app.route("/cities", methods=["POST"])
def create_city():
    if not request.is_json:
        abort(400, description="Request must be JSON")

    data = request.get_json()
    name = data.get("name")
    country_code = data.get("country_code")

    if not name or not country_code:
        abort(400, description="Missing required fields: name and country_code")

    if country_code.upper() not in countries:
        abort(400, description="Invalid country code")

    city_id = get_next_city_id()
    cities[city_id] = {
        "name": name,
        "country_code": country_code.upper()
    }

    return jsonify({"id": city_id, "name": name, "country_code": country_code.upper()}), 201

@app.route("/cities/<int:city_id>", methods=["GET"])
def get_city_by_id(city_id):
    city = cities.get(city_id)
    if not city:
        abort(404, description="City not found")

    return jsonify(city)

@app.route("/cities/<int:city_id>", methods=["PUT"])
def update_city(city_id):
    if not request.is_json:
        abort(400, description="Request must be JSON")

    data = request.get_json()
    name = data.get("name")
    country_code = data.get("country_code")

    if not name or not country_code:
        abort(400, description="Missing required fields: name and country_code")

    if country_code.upper() not in countries:
        abort(400, description="Invalid country code")

    city = cities.get(city_id)
    if not city:
        abort(404, description="City not found")

    city["name"] = name
    city["country_code"] = country_code.upper()

    return jsonify(city)