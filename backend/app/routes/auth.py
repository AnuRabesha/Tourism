from flask import Blueprint, request, jsonify
import re

auth_bp = Blueprint("auth", __name__)

# In-memory user store — replace with PostgreSQL in production
# Format: { email: { mobile, password_hash } }
USERS = {}


def _valid_mobile(m):
    return bool(re.match(r"^[6-9]\d{9}$", str(m).strip()))


def _valid_email(e):
    return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", str(e).strip()))


def _valid_password(p):
    return len(str(p)) >= 6


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    mobile   = str(data.get("mobile", "")).strip()
    email    = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not _valid_mobile(mobile):
        return jsonify({"error": "Invalid mobile number. Must be 10 digits starting with 6-9."}), 400
    if not _valid_email(email):
        return jsonify({"error": "Invalid email address."}), 400
    if not _valid_password(password):
        return jsonify({"error": "Password must be at least 6 characters."}), 400
    if email in USERS:
        return jsonify({"error": "Email already registered."}), 409

    USERS[email] = {"mobile": mobile, "password": password}
    return jsonify({"success": True, "message": "Registration successful."}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    mobile   = str(data.get("mobile", "")).strip()
    email    = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    # Validate format first
    if not _valid_mobile(mobile):
        return jsonify({"error": "Invalid mobile number."}), 400
    if not _valid_email(email):
        return jsonify({"error": "Invalid email address."}), 400
    if not _valid_password(password):
        return jsonify({"error": "Password must be at least 6 characters."}), 400

    # Check credentials
    user = USERS.get(email)
    if not user:
        # Auto-register on first login for demo purposes
        USERS[email] = {"mobile": mobile, "password": password}
        return jsonify({"success": True, "name": email.split("@")[0], "message": "Welcome! Account created."}), 200

    if user["password"] != password:
        return jsonify({"error": "Incorrect password."}), 401
    if user["mobile"] != mobile:
        return jsonify({"error": "Mobile number does not match."}), 401

    return jsonify({"success": True, "name": email.split("@")[0], "message": "Login successful."}), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({"success": True, "message": "Logged out."}), 200
