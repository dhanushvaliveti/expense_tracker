from flask import Blueprint,request, jsonify
from extensions import db
from models import User,Category,Expense
from middlewares.auth import auth_required

"""expenses routes post,get,put,delete"""
expenses_bp=Blueprint("expenses",__name__)
@expenses_bp.route("/categories/<int:category_id>/expenses",methods=["POST"])
@auth_required
def Create_expense(category_id):
    data=request.get_json()
    if data is None or "amount" not in data or "desc" not in data or "date" not in data:
        return jsonify({"error":"name is not given"}),400
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({"error": "category not found"}), 404
    expenses=Expense(amount=data["amount"],desc=data["desc"],date=data["date"],category_id=category.id)
    db.session.add(expenses)
    db.session.commit()
    return jsonify({"id":expenses.id,"amount":expenses.amount,"desc":expenses.desc,"date":expenses.date,"category_id":expenses.category_id}),201

@expenses_bp.route("/categories/<int:category_id>/expenses")
@auth_required
def show_expense(category_id):
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({"error": "category not found"}), 404
    res=[]
    for i in category.expenses:
        res.append({"id":i.id,"amount":i.amount,"desc":i.desc,"date":i.date,"category_id":i.category_id})
    return jsonify(res),200
   
@expenses_bp.route("/expenses/<int:expense_id>",methods=["PUT"])
@auth_required
def Update_expense(expense_id):
    data=request.get_json()
    if data is None:
        return jsonify({"error":"data is not given"}),400
    expenses=Expense.query.get(expense_id)
    if expenses is None :
        return jsonify({"error":" is not given"}),400
        
    if "amount" in data:
        expenses.amount = data["amount"]
    if "desc" in data:
        expenses.desc = data["desc"]

    db.session.commit()
    return jsonify({"id":expenses.id,"amount":expenses.amount,"desc":expenses.desc,"date":expenses.date,"category_id":expenses.category_id}),201
    
@expenses_bp.route("/expenses/<int:expense_id>",methods=["DELETE"])
@auth_required
def Delete_expense(expense_id):
    expenses=Expense.query.get(expense_id)
    if expenses is None:
        return jsonify({"error": "expense not found"}), 404
    db.session.delete(expenses)
    db.session.commit()
    return "",204
    
    
@expenses_bp.route("/total-expenses", methods=["GET"])
@auth_required
def total_expenses():
    user_id = request.user_id
    from models import Expense, Category

    expenses = (
        Expense.query
        .join(Category, Expense.category_id == Category.id)
        .filter(Category.user_id == user_id)
        .all()
    )

    total = sum(exp.amount for exp in expenses)

    return jsonify({
        "user_id": user_id,
        "total_expense": total
    }), 200
