from flask import Blueprint, request, jsonify
import requests, os

weather_bp = Blueprint("weather", __name__)

BASE_URL = "https://api.openweathermap.org/data/2.5"

def _api_key():
    return os.getenv("WEATHER_API_KEY")

@weather_bp.route("/current", methods=["GET"])
def current_weather():
    """Current weather by city name or lat/lng."""
    city = request.args.get("city")
    lat = request.args.get("lat")
    lng = request.args.get("lng")

    if city:
        params = {"q": city, "appid": _api_key(), "units": "metric"}
    elif lat and lng:
        params = {"lat": lat, "lon": lng, "appid": _api_key(), "units": "metric"}
    else:
        return jsonify({"error": "Provide city or lat/lng"}), 400

    if not _api_key():
        return jsonify({"error": "WEATHER_API_KEY not set in .env"}), 500

    try:
        resp = requests.get(f"{BASE_URL}/weather", params=params, timeout=10)
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Weather service unavailable: {str(e)}"}), 503


@weather_bp.route("/forecast", methods=["GET"])
def forecast():
    """5-day weather forecast."""
    city = request.args.get("city")
    lat = request.args.get("lat")
    lng = request.args.get("lng")

    if city:
        params = {"q": city, "appid": _api_key(), "units": "metric"}
    elif lat and lng:
        params = {"lat": lat, "lon": lng, "appid": _api_key(), "units": "metric"}
    else:
        return jsonify({"error": "Provide city or lat/lng"}), 400

    if not _api_key():
        return jsonify({"error": "WEATHER_API_KEY not set in .env"}), 500

    try:
        resp = requests.get(f"{BASE_URL}/forecast", params=params, timeout=10)
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Weather service unavailable: {str(e)}"}), 503
