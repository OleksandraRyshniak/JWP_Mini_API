
import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY puudub .env failist")

ALGORITHM = "HS256"
TOKEN_MINUTES = 5

USERS = {
    "student": {
        "password": "student123",
        "id": "1024",
        "role": "student"
    },
    "admin": {
        "password": "admin123",
        "id": "1",
        "role": "admin"
    }
}


def token_required(admin_only=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", "")
            parts = auth.split()

            if len(parts) != 2 or parts[0].lower() != "bearer":
                return jsonify({"error": "Token puudub"}), 401

            try:
                data = jwt.decode(
                    parts[1],
                    SECRET_KEY,
                    algorithms=[ALGORITHM],
                    options={"require": ["sub", "role", "exp"]}
                )
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token aegunud"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Vigane token"}), 401

            if admin_only and data["role"] != "admin":
                return jsonify({"error": "Ligipääs keelatud"}), 403

            return func(data, *args, **kwargs)

        return wrapper
    return decorator


@app.post("/login")
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Vigased sisendandmed"}), 400

    username = data.get("username")
    password = data.get("password")

    user = USERS.get(username) if isinstance(username, str) else None

    if not user or user["password"] != password:
        return jsonify({"error": "Vale kasutajanimi või parool"}), 401

    expiration = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_MINUTES
    )

    token = jwt.encode(
        {
            "sub": user["id"],
            "role": user["role"],
            "exp": expiration
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return jsonify({"access_token": token}), 200


@app.get("/profiil")
@token_required()
def profile(data):
    return jsonify({
        "message": "Profiili andmed",
        "user_id": data["sub"],
        "role": data["role"]
    }), 200


@app.get("/admin")
@token_required(admin_only=True)
def admin(data):
    return jsonify({
        "message": "Administraatori ligipääs lubatud",
        "user_id": data["sub"]
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
