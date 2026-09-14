from flask import Blueprint, request, jsonify
import requests, os
from datetime import datetime

weather_bp = Blueprint("weather", __name__)
BASE_URL = "https://api.openweathermap.org/data/2.5"

DEMO_WEATHER = {
    "cod": 200, "name": "Chennai",
    "main": {"temp": 32, "feels_like": 36, "humidity": 78},
    "weather": [{"description": "partly cloudy", "main": "Clouds"}],
    "wind": {"speed": 4.5}, "_demo": True
}
DEMO_FORECAST = {
    "cod": "200",
    "list": [
        {"dt": 1700000000 + i * 10800,
         "main": {"temp": 28 + (i % 5), "humidity": 70},
         "weather": [{"description": "partly cloudy", "main": "Clouds"}],
         "wind": {"speed": 3.5}, "pop": 0.1 if i % 8 < 2 else 0.0}
        for i in range(40)
    ], "_demo": True
}

CROWD_DATA = {
    "marina beach": "low", "taj mahal": "high", "kodaikanal": "low",
    "ooty": "medium", "rameswaram": "low", "madurai meenakshi": "high",
    "gateway of india": "high", "mysore palace": "medium"
}


def _api_key():
    key = os.getenv("WEATHER_API_KEY", "")
    return None if key in ("", "your_openweathermap_api_key") else key


def _smart_analysis(temp, humidity, wind_speed, rain_prob, description):
    desc = description.lower()
    is_rainy = rain_prob > 0.4 or "rain" in desc or "drizzle" in desc
    is_stormy = "storm" in desc or "thunder" in desc or wind_speed > 12
    is_hot = temp > 35
    is_cold = temp < 15
    is_hazy = "haze" in desc or "fog" in desc or "mist" in desc

    # Suitability score
    score = 100
    if is_rainy: score -= 30
    if is_stormy: score -= 40
    if is_hot: score -= 20
    if is_cold: score -= 10
    if humidity > 85: score -= 10
    if wind_speed > 8: score -= 10
    score = max(0, score)

    if score >= 80: score_label, score_emoji = "Excellent for visiting", "🌟"
    elif score >= 60: score_label, score_emoji = "Good for visiting", "✅"
    elif score >= 40: score_label, score_emoji = "Fair – plan carefully", "⚠️"
    else: score_label, score_emoji = "Poor – avoid outdoor activities", "❌"

    # Best time
    if is_hot:
        best_time = "Early morning (6–9 AM) or evening (5–7 PM)"
    elif is_rainy:
        best_time = "Mid-morning (10 AM–12 PM) if rain clears"
    else:
        best_time = "Morning (8–11 AM) or late afternoon (4–7 PM)"

    # Activities
    activities = {
        "🏖️ Beach": "✅ Great" if not is_stormy and not is_rainy and wind_speed < 8 else "❌ Avoid",
        "🥾 Trekking": "✅ Great" if not is_rainy and not is_hot and not is_stormy else "❌ Avoid",
        "🛕 Temple Visits": "✅ Good" if not is_stormy else ("🌧️ Carry umbrella" if is_rainy else "✅ Good"),
        "📸 Sightseeing": "✅ Perfect" if score >= 60 and not is_hazy else ("🌫️ Hazy" if is_hazy else "⚠️ Limited"),
        "🚤 Boating": "✅ Safe" if wind_speed < 6 and not is_stormy and not is_rainy else "❌ Not safe",
    }

    # What to carry
    carry = []
    if is_rainy or rain_prob > 0.3: carry.append("☂️ Umbrella")
    if is_hot or temp > 30: carry.append("🧴 Sun protection"); carry.append("💧 Water bottle")
    if is_cold: carry.append("🧥 Light jacket")
    if wind_speed > 7: carry.append("🧣 Windbreaker")
    if is_hazy: carry.append("😷 Face mask")
    if not carry: carry.append("😊 Nothing special – enjoy your trip!")

    # Extreme warnings
    warnings = []
    if is_stormy: warnings.append("⚠️ Thunderstorm alert – stay indoors")
    if temp > 40: warnings.append("🔥 Heatwave warning – avoid outdoor exposure")
    if temp < 10: warnings.append("🥶 Cold wave – dress warmly")
    if wind_speed > 12: warnings.append("💨 Strong winds – avoid coastal areas")
    if rain_prob > 0.7: warnings.append("🌧️ Heavy rain likely – carry rain gear")

    # Personalized travel alert
    if is_hot:
        travel_alert = "🌡️ Hot day ahead. Start sightseeing before 10 AM and rest during 12–4 PM."
    elif is_rainy:
        travel_alert = "🌧️ Rain expected. Carry an umbrella and wear waterproof footwear."
    elif is_stormy:
        travel_alert = "⛈️ Storm warning! Postpone outdoor plans and stay safe indoors."
    elif score >= 80:
        travel_alert = "🌤️ Perfect weather today! Great day to explore outdoor attractions."
    else:
        travel_alert = "🌥️ Moderate weather. Plan indoor and outdoor activities in balance."

    return {
        "score": score, "score_label": score_label, "score_emoji": score_emoji,
        "best_time": best_time, "activities": activities,
        "carry": carry, "warnings": warnings, "travel_alert": travel_alert
    }


@weather_bp.route("/current", methods=["GET"])
def current_weather():
    city = request.args.get("city")
    lat, lng = request.args.get("lat"), request.args.get("lng")
    if city:
        params = {"q": city, "appid": _api_key(), "units": "metric"}
    elif lat and lng:
        params = {"lat": lat, "lon": lng, "appid": _api_key(), "units": "metric"}
    else:
        return jsonify({"error": "Provide city or lat/lng"}), 400
    if not _api_key():
        return jsonify(DEMO_WEATHER), 200
    try:
        resp = requests.get(f"{BASE_URL}/weather", params=params, timeout=10)
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Weather service unavailable: {str(e)}"}), 503


@weather_bp.route("/forecast", methods=["GET"])
def forecast():
    city = request.args.get("city")
    lat, lng = request.args.get("lat"), request.args.get("lng")
    if city:
        params = {"q": city, "appid": _api_key(), "units": "metric"}
    elif lat and lng:
        params = {"lat": lat, "lon": lng, "appid": _api_key(), "units": "metric"}
    else:
        return jsonify({"error": "Provide city or lat/lng"}), 400
    if not _api_key():
        return jsonify(DEMO_FORECAST), 200
    try:
        resp = requests.get(f"{BASE_URL}/forecast", params=params, timeout=10)
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Weather service unavailable: {str(e)}"}), 503


@weather_bp.route("/smart", methods=["GET"])
def smart_weather():
    city = request.args.get("city", "Chennai")
    if not _api_key():
        analysis = _smart_analysis(32, 78, 4.5, 0.1, "partly cloudy")
        crowd = CROWD_DATA.get(city.lower(), "medium")
        analysis["city"] = city
        analysis["crowd"] = crowd
        analysis["rain_alert"] = None
        analysis["place_recommendation"] = _place_recommendation(city, "partly cloudy", 32)
        return jsonify(analysis), 200
    try:
        r = requests.get(f"{BASE_URL}/weather", params={"q": city, "appid": _api_key(), "units": "metric"}, timeout=10)
        fr = requests.get(f"{BASE_URL}/forecast", params={"q": city, "appid": _api_key(), "units": "metric", "cnt": 4}, timeout=10)
        w = r.json()
        f = fr.json()
        if str(w.get("cod")) != "200":
            return jsonify({"error": w.get("message", "City not found")}), 404
        temp = w["main"]["temp"]
        humidity = w["main"]["humidity"]
        wind = w["wind"]["speed"]
        desc = w["weather"][0]["description"]
        rain_prob = max((e.get("pop", 0) for e in f.get("list", [])), default=0)
        analysis = _smart_analysis(temp, humidity, wind, rain_prob, desc)
        analysis["city"] = w["name"]
        analysis["crowd"] = CROWD_DATA.get(city.lower(), "medium")
        analysis["rain_alert"] = "🌧️ Rain likely in the next few hours. Carry an umbrella!" if rain_prob > 0.4 else None
        analysis["place_recommendation"] = _place_recommendation(city, desc, temp)
        return jsonify(analysis), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 503


def _place_recommendation(city, desc, temp):
    desc = desc.lower()
    if "rain" in desc or "drizzle" in desc:
        return f"🌧️ Rainy in {city}? Try nearby museums, temples, or shopping malls."
    if temp > 36:
        return f"🔥 Too hot in {city}? Visit hill stations like Ooty or Kodaikanal nearby."
    if "clear" in desc or "sunny" in desc:
        return f"☀️ Clear skies in {city}! Perfect for beaches, parks and outdoor sightseeing."
    return f"🌤️ Good weather in {city}. Explore local attractions and heritage sites."
