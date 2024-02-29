#!/usr/bin/python3
"""returns status of server"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """returns jsonified status"""
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def stats():
    """retrieves the number of each objects by type"""
    retrieval = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
    }
    return jsonify(retrieval)
