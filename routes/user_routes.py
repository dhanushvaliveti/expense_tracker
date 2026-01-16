from flask import Blueprint,request, jsonify
from extensions import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from middlewares.auth import auth_required
import jwt
from datetime import datetime, timedelta


""" user routes post and get"""
user_bp = Blueprint("users", __name__)
@user_bp.route("/users",methods=["POST"])
@auth_required
def Create_user():
    data=request.get_json()
    if data is None or "name" not in data:
        return jsonify({"error":"name is not given"}),400
    user=User(name=data["name"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"id":user.id,"name":user.name}),201
@user_bp.route("/users")
@auth_required
def Show_user():
    user=User.query.all()
    res=[]
    for i in user:
        res.append({"id":i.id,"name":i.name})
    return jsonify(res),200
@user_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    if data is None or "name" not in data or "password" not in data:
        return jsonify({"error": "name and password required"}), 400

    existing_user = User.query.filter_by(name=data["name"]).first()
    if existing_user:
        return jsonify({"error": "user already exists"}), 409

    hashed_password = generate_password_hash(data["password"])

    user = User(
        name=data["name"],
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "name": user.name
    }), 201
@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "name" not in data or "password" not in data:
        return jsonify({"error": "name and password required"}), 400

    user = User.query.filter_by(name=data["name"]).first()

    if not user:
        return jsonify({"error": "user not found"}), 404

    if not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "incorrect password"}), 401


    SECRET_KEY = "MYSECRET"

    token = jwt.encode(
        {
            "user_id": user.id,
            "name": user.name,
            "exp": datetime.utcnow() + timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"message": "login successful","token": token,"user_id": user.id}), 200


