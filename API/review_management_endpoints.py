from flask import Flask
from flask import jsonify
from flask import request, abort
from Persistence.data_manager import data_manager
from API.endpoints_methods import save_data, load_data, app
import json

reviews = {}

@app.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    data = request.get_json()
    print("test")
    if not data or "user_id" not in data or "text" not in data:
        print("missing fields")
        abort(400, description="Missing required fields: user_id, text")
    if not isinstance(data["user_id"], str) or not isinstance(data["text"], str):
        print("invalid format")
        abort(400, description="Invalid input format")
    if not data_manager.exists(data["user_id"], "User"):
        print("user not found")
        abort(404, description="User not found")
    if not data_manager.exists(place_id, "Place"):
        print("404")
        abort(404, description="Place not found")
    entity = data_manager.create("Review", **data)
    print("2")
    data['id'] = entity.id
    print("3")
    save_data(data, "Persistence/reviews.json")
    print("4")
    # Respond with the newly created review
    return jsonify({'id': entity.id}), 201

@app.route("/users/<user_id>/reviews", methods=["GET"])
def get_reviews_by_user(user_id):
    all_reviews = load_data("Persistence/reviews.json")
    user_reviews = []
    for review in all_reviews:
        if review["user_id"] == user_id:
            user_reviews.append(review)
    return jsonify(user_reviews)

@app.route("/places/<place_id>/reviews/<review_id>", methods=["GET"])
def get_review_by_id(place_id, review_id):
    all_reviews = load_data("Persistence/reviews.json")
    for review in all_reviews:
        if review["id"] == review_id and review["place_id"] == place_id:
            return review
    return None

@app.route("/reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    all_reviews = load_data("Persistence/reviews.json")
    for review in all_reviews:
        if review["id"] == review_id:
            return review
    return None

@app.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    all_reviews = load_data("Persistence/reviews.json")
    for review in all_reviews:
        if review["id"] == review_id:
            data = request.get_json()
            review["text"] = data["text"]
            with open("Persistence/reviews.json", 'w') as f:
                json.dump(all_reviews, f)
            return jsonify(review)
    abort(404, description="Review not found")

@app.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    all_reviews = load_data("Persistence/reviews.json")
    for review in all_reviews:
        if review["id"] == review_id:
            all_reviews.remove(review)
            with open("Persistence/reviews.json", 'w') as f:
                json.dump(all_reviews, f)
            return jsonify(review)
    return None


