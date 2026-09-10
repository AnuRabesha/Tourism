from flask import Blueprint, request, jsonify

food_bp = Blueprint("food", __name__)

# Static data — extend with DB integration as needed
TEMPLE_FOOD = [
    {"name": "Tirupati Temple", "location": "Tirupati, AP", "timings": "6 AM – 8 PM", "free": True},
    {"name": "Golden Temple", "location": "Amritsar, Punjab", "timings": "All day", "free": True},
    {"name": "Shirdi Sai Baba Temple", "location": "Shirdi, MH", "timings": "7 AM – 9 PM", "free": True},
    {"name": "Meenakshi Temple", "location": "Madurai, TN", "timings": "5 AM – 9 PM", "free": True},
]

FAMOUS_DISHES = {
    "Tamil Nadu": ["Idli Sambar", "Chettinad Chicken", "Pongal", "Dosa", "Filter Coffee"],
    "Kerala": ["Appam with Stew", "Kerala Fish Curry", "Puttu & Kadala", "Sadya"],
    "Punjab": ["Butter Chicken", "Dal Makhani", "Sarson da Saag", "Lassi"],
    "Rajasthan": ["Dal Baati Churma", "Laal Maas", "Ghevar"],
    "West Bengal": ["Rosogolla", "Macher Jhol", "Mishti Doi"],
    "Maharashtra": ["Vada Pav", "Puran Poli", "Misal Pav"],
}


@food_bp.route("/temple-food", methods=["GET"])
def temple_food():
    """List temples offering free food."""
    state = request.args.get("state")
    if state:
        filtered = [t for t in TEMPLE_FOOD if state.lower() in t["location"].lower()]
        return jsonify(filtered)
    return jsonify(TEMPLE_FOOD)


@food_bp.route("/famous-dishes", methods=["GET"])
def famous_dishes():
    """Get famous dishes. Optional ?state= filter."""
    state = request.args.get("state")
    if state:
        dishes = FAMOUS_DISHES.get(state)
        if not dishes:
            return jsonify({"error": "State not found", "available": list(FAMOUS_DISHES.keys())}), 404
        return jsonify({"state": state, "dishes": dishes})
    return jsonify(FAMOUS_DISHES)
