from flask import Blueprint,request, jsonify
from extensions import db
from models import User, Category
from middlewares.auth import auth_required

""" categories routes post and get"""
category_bp=Blueprint("categories",__name__)
@category_bp.route("/users/<int:user_id>/categories",methods=["POST"])
@auth_required
def Create_category(user_id):
    data=request.get_json()
    if data is None or "food" not in data:
        return jsonify({"error":"name is not given"}),400
    user=User.query.get(user_id)
    if user is None:
        return jsonify({"error": "user not found"}), 404
    categories=Category(food=data["food"],user_id=user.id)
    db.session.add(categories)
    db.session.commit()
    return jsonify({"id":categories.id,"food":categories.food,"user_id":categories.user_id}),201
@category_bp.route("/users/<int:user_id>/categories")
@auth_required
def Show_category(user_id):
    user=User.query.get(user_id)
    if user is None:
        return jsonify({"error": "user not found"}), 404
    
    res=[]
    for i in user.categories:
        res.append({"id":i.id,"food":i.food,"user_id":i.user_id})
    return jsonify(res),200
