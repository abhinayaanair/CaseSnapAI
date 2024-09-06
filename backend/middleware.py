from flask import request, jsonify
from functools import wraps

def require_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Missing authentication token"}), 401

        # Here you would usually decode and validate the token
        # For simplicity, this example assumes a hardcoded token
        if token != "your_secret_token":
            return jsonify({"message": "Invalid authentication token"}), 403

        return f(*args, **kwargs)

    return decorated_function
