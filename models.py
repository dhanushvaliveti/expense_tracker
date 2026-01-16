from extensions import db
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    categories=db.relationship("Category",backref="user",lazy=True)
    password = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(200))

class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    food=db.Column(db.String(200),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    expenses=db.relationship("Expense",backref="category",lazy=True)
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount=db.Column(db.Integer,nullable=False)
    desc=db.Column(db.String(200),nullable=False)
    date=db.Column(db.String(200),nullable=False)
    category_id = db.Column(db.Integer,db.ForeignKey("category.id"),nullable=False)
