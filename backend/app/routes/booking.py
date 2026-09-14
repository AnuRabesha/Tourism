from flask import Blueprint, request, jsonify
from datetime import datetime, timezone

booking_bp = Blueprint("booking", __name__)

_bookings = []
_booking_id_counter = [1]


def _next_id():
    bid = _booking_id_counter[0]
    _booking_id_counter[0] += 1
    return bid


HOTELS = [
    {
        "id": 1, "name": "Grand Palace Hotel", "city": "Chennai",
        "price_per_night": 2500, "rating": 4.5,
        "rooms": [
            {"type": "Standard", "available": 5, "price": 2500},
            {"type": "Deluxe", "available": 3, "price": 3500},
            {"type": "Suite", "available": 1, "price": 6000},
        ],
        "amenities": ["WiFi", "AC", "Restaurant", "Parking"],
        "instant_food": ["Idli", "Dosa", "Poori", "Upma", "Filter Coffee"]
    },
    {
        "id": 2, "name": "Heritage Inn", "city": "Madurai",
        "price_per_night": 1800, "rating": 4.2,
        "rooms": [
            {"type": "Standard", "available": 8, "price": 1800},
            {"type": "Deluxe", "available": 4, "price": 2800},
            {"type": "Suite", "available": 0, "price": 5000},
        ],
        "amenities": ["WiFi", "AC", "Room Service"],
        "instant_food": ["Parotta", "Biryani", "Chettinad Curry", "Tea", "Samosa"]
    },
    {
        "id": 3, "name": "Backwater Resort", "city": "Alleppey",
        "price_per_night": 3200, "rating": 4.7,
        "rooms": [
            {"type": "Standard", "available": 2, "price": 3200},
            {"type": "Deluxe", "available": 2, "price": 4500},
            {"type": "Suite", "available": 1, "price": 8000},
        ],
        "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Boat Ride"],
        "instant_food": ["Appam", "Fish Curry", "Puttu", "Kerala Meals", "Coconut Water"]
    },
    {
        "id": 4, "name": "Desert Camp", "city": "Jaisalmer",
        "price_per_night": 2000, "rating": 4.3,
        "rooms": [
            {"type": "Tent Standard", "available": 10, "price": 2000},
            {"type": "Tent Deluxe", "available": 5, "price": 3000},
            {"type": "Suite", "available": 0, "price": 5500},
        ],
        "amenities": ["Bonfire", "Camel Ride", "Folk Music", "Meals Included"],
        "instant_food": ["Dal Baati", "Churma", "Lassi", "Chai", "Rajasthani Thali"]
    },
    {
        "id": 5, "name": "Temple View Lodge", "city": "Tiruvannamalai",
        "price_per_night": 1200, "rating": 4.0,
        "rooms": [
            {"type": "Standard", "available": 12, "price": 1200},
            {"type": "Deluxe", "available": 6, "price": 2000},
            {"type": "Suite", "available": 2, "price": 3500},
        ],
        "amenities": ["WiFi", "AC", "Temple View", "Vegetarian Restaurant"],
        "instant_food": ["Pongal", "Idli Sambar", "Vada", "Payasam", "Buttermilk"]
    },
    {
        "id": 6, "name": "Marina Beach Hotel", "city": "Chennai",
        "price_per_night": 3500, "rating": 4.6,
        "rooms": [
            {"type": "Standard", "available": 0, "price": 3500},
            {"type": "Deluxe", "available": 4, "price": 5000},
            {"type": "Suite", "available": 2, "price": 9000},
        ],
        "amenities": ["WiFi", "Sea View", "Pool", "Gym", "Restaurant"],
        "instant_food": ["Sundal", "Murukku", "Bajji", "Juice", "South Indian Meals"]
    },
]


@booking_bp.route("/hotels", methods=["GET"])
def list_hotels():
    city = request.args.get("city", "").lower()
    result = HOTELS
    if city:
        result = [h for h in result if city in h["city"].lower()]
    # Add availability summary
    for h in result:
        h["total_available"] = sum(r["available"] for r in h["rooms"])
    return jsonify(result)


@booking_bp.route("/hotels/<int:hotel_id>", methods=["GET"])
def hotel_detail(hotel_id):
    hotel = next((h for h in HOTELS if h["id"] == hotel_id), None)
    if not hotel:
        return jsonify({"error": "Hotel not found"}), 404
    hotel["total_available"] = sum(r["available"] for r in hotel["rooms"])
    return jsonify(hotel)


@booking_bp.route("/transport", methods=["GET"])
def transport_options():
    """Get transport options between two cities."""
    origin = request.args.get("origin")
    destination = request.args.get("destination")
    if not origin or not destination:
        return jsonify({"error": "origin and destination are required"}), 400

    # Static sample — integrate with real transport API as needed
    options = [
        {"type": "Bus", "operator": "TNSTC", "duration": "6h", "price": 350},
        {"type": "Train", "operator": "Indian Railways", "duration": "4h", "price": 500},
        {"type": "Flight", "operator": "IndiGo", "duration": "1h", "price": 3500},
    ]
    return jsonify({"origin": origin, "destination": destination, "options": options})


@booking_bp.route("/pre-book", methods=["POST"])
def pre_book():
    """Pre-book a hotel or transport. Body: {type, name, user_name, date, guests}"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    required = ["type", "name", "user_name", "date"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    # Validate guests is a positive integer
    try:
        guests = int(data.get("guests", 1))
        if guests < 1:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "guests must be a positive integer"}), 400

    booking = {
        "booking_id": _next_id(),
        "type": data["type"],
        "name": data["name"],
        "user_name": data["user_name"],
        "date": data["date"],
        "guests": guests,
        "booked_at": datetime.now(timezone.utc).isoformat(),
        "status": "confirmed",
    }
    _bookings.append(booking)
    return jsonify({"message": "Booking confirmed", "booking": booking}), 201


@booking_bp.route("/bookings/<user_name>", methods=["GET"])
def get_bookings(user_name):
    """Get all bookings for a user."""
    user_bookings = [b for b in _bookings if b["user_name"] == user_name]
    return jsonify(user_bookings)
