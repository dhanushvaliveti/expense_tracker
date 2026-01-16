from functools import wraps
from flask import request, jsonify
import jwt

SECRET_KEY = "MYSECRET"  # use your secret

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Missing token"}), 401

        # Token should be in format: Bearer <token>
        try:
            if token.startswith("Bearer "):
                token = token.split(" ")[1]

            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated

