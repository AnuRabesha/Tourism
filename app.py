from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import traceback

from routes.live_data import live_data_bp
from routes.weather import weather_bp
from routes.safety import safety_bp
from routes.language import language_bp
from routes.food import food_bp
from routes.booking import booking_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

# Register all blueprints with versioned prefix
app.register_blueprint(live_data_bp, url_prefix="/api/live-data")
app.register_blueprint(weather_bp,   url_prefix="/api/weather")
app.register_blueprint(safety_bp,    url_prefix="/api/safety")
app.register_blueprint(language_bp,  url_prefix="/api/language")
app.register_blueprint(food_bp,      url_prefix="/api/food")
app.register_blueprint(booking_bp,   url_prefix="/api/booking")


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "app": "Tourism Support API"})


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def internal_error(e):
    traceback.print_exc()
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
