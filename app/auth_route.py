from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import users_collection
import uuid
import datetime

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if (
        not data
        or not data.get("email")
        or not data.get("password")
        or not data.get("full_name")
    ):
        return jsonify(
            {
                "message": "Please provide all required fields: full_name, email, and password"
            }
        ), 400

    email = data["email"]
    existing_user = users_collection.find_one({"email": email})
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")

    user = {
        "_id": str(uuid.uuid4()),
        "full_name": data["full_name"],
        "email": email,
        "password": hashed_password,
        "created_at": datetime.datetime.utcnow(),
    }

    users_collection.insert_one(user)
    return jsonify({"message": "User created successfully"}), 201


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Please provide both email and password"}), 400

    user = users_collection.find_one({"email": data["email"]})
    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user["_id"])
    return jsonify({"access_token": access_token}), 200


@auth.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = users_collection.find_one(
        {"_id": user_id}, {"password": 0}
    )  # Do not return the password
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"user": user}), 200
