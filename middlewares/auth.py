from functools import wraps
from flask import request, jsonify
import jwt

SECRET_KEY = "MYSECRET"

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Missing token"}), 401

        try:
            if token.startswith("Bearer "):
                token = token.split(" ")[1]

            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_id = data["user_id"]  

        except Exception:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated
