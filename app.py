from flask import Flask, jsonify, send_from_directory, abort, request
from flask_cors import CORS
from dotenv import load_dotenv
import traceback, os, re

load_dotenv()

from routes.live_data import live_data_bp
from routes.weather   import weather_bp
from routes.safety    import safety_bp
from routes.language  import language_bp
from routes.food      import food_bp
from routes.booking   import booking_bp

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

app = Flask(__name__, static_folder=None)
CORS(app)

# ── API Blueprints ──────────────────────────────────────────────────────────
app.register_blueprint(live_data_bp, url_prefix="/api/live-data")
app.register_blueprint(weather_bp,   url_prefix="/api/weather")
app.register_blueprint(safety_bp,    url_prefix="/api/safety")
app.register_blueprint(language_bp,  url_prefix="/api/language")
app.register_blueprint(food_bp,      url_prefix="/api/food")
app.register_blueprint(booking_bp,   url_prefix="/api/booking")

# ── In-memory auth store ────────────────────────────────────────────────────
USERS = {}

def _valid_mobile(m): return bool(re.match(r"^[6-9]\d{9}$", str(m).strip()))
def _valid_email(e):  return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", str(e).strip()))
def _valid_pw(p):     return len(str(p)) >= 6

@app.route("/api/auth/register", methods=["POST"])
def register():
    d = request.get_json(silent=True) or {}
    mobile, email, pw = str(d.get("mobile","")).strip(), str(d.get("email","")).strip().lower(), str(d.get("password",""))
    if not _valid_mobile(mobile): return jsonify({"error":"Invalid mobile number."}), 400
    if not _valid_email(email):   return jsonify({"error":"Invalid email address."}), 400
    if not _valid_pw(pw):         return jsonify({"error":"Password must be at least 6 characters."}), 400
    if email in USERS:            return jsonify({"error":"Email already registered."}), 409
    USERS[email] = {"mobile": mobile, "password": pw}
    return jsonify({"success": True, "message": "Registration successful."}), 201

@app.route("/api/auth/login", methods=["POST"])
def login():
    d = request.get_json(silent=True) or {}
    mobile, email, pw = str(d.get("mobile","")).strip(), str(d.get("email","")).strip().lower(), str(d.get("password",""))
    if not _valid_mobile(mobile): return jsonify({"error":"Invalid mobile number."}), 400
    if not _valid_email(email):   return jsonify({"error":"Invalid email address."}), 400
    if not _valid_pw(pw):         return jsonify({"error":"Password must be at least 6 characters."}), 400
    user = USERS.get(email)
    if not user:
        USERS[email] = {"mobile": mobile, "password": pw}
        return jsonify({"success": True, "name": email.split("@")[0], "message": "Welcome! Account created."}), 200
    if user["password"] != pw or user["mobile"] != mobile:
        return jsonify({"error":"Invalid credentials."}), 401
    return jsonify({"success": True, "name": email.split("@")[0], "message": "Login successful."}), 200

@app.route("/api/auth/logout", methods=["POST"])
def logout():
    return jsonify({"success": True}), 200

# ── Health ──────────────────────────────────────────────────────────────────
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "app": "TourEase API", "version": "2.0"})

# ── Serve login page ────────────────────────────────────────────────────────
@app.route("/login")
def serve_login():
    return send_from_directory(os.path.join(FRONTEND_DIR, "pages"), "login.html")

# ── Serve frontend static assets ────────────────────────────────────────────
@app.route("/static/frontend/<path:filename>")
def frontend_static(filename):
    return send_from_directory(FRONTEND_DIR, filename)

# ── Serve frontend pages ─────────────────────────────────────────────────────
@app.route("/pages/<page>")
def serve_page(page):
    return send_from_directory(os.path.join(FRONTEND_DIR, "pages"), page)

# ── Serve home ───────────────────────────────────────────────────────────────
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path:
        frontend_abs = os.path.realpath(FRONTEND_DIR)
        target = os.path.realpath(os.path.join(FRONTEND_DIR, path))
        if not target.startswith(frontend_abs + os.sep) and target != frontend_abs:
            abort(404)
        if os.path.isfile(target):
            return send_from_directory(os.path.dirname(target), os.path.basename(target))
    return send_from_directory(FRONTEND_DIR, "index.html")

# ── Error handlers ────────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):    return jsonify({"error": "Not found"}), 404
@app.errorhandler(500)
def server_error(e): traceback.print_exc(); return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
