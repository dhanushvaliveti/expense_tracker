from flask import Flask,request,jsonify
from extensions import db
from routes.user_routes import user_bp
from routes.category_routes import category_bp
from routes.expenses_routes import expenses_bp
def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///users.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(user_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(expenses_bp)
    return app
app=create_app()
if __name__=="__main__":
    app.run(debug=True)

