#!/usr/bin/python3
"""api module concearned with cities module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'])
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    all_states = storage.all('Amenity')
    values = [val.to_dict() for val in all_states.values()]
    return jsonify(values)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """retrieves a Amenity object"""
    value = storage.get('Amenity', amenity_id)
    return jsonify(value.to_dict()) if value is not None else abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """deletes an amenity"""
    value = storage.get('Amenity', amenity_id)
    abort(404) if value is None else value.delete()
    storage.save()
    return jsonify({})


@app_views.route("/amenities", methods=['POST'])
def post_amenity():
    """posts data to existing json blob"""
    if not request.get_json():
        return jsonify({"error: Not a JSON"}), 400
    blob = request.get_json()
    if 'name' not in blob:
        return jsonify({"error: Missing name"}), 400
    """create it using the blob data"""
    newObject = Amenity(**blob)
    """save it to persist in memory"""
    newObject.save()
    return jsonify(newObject.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def put_amenity(amenity_id):
    """updates Amenity object"""
    if not request.get_json():
        return jsonify({"error: Not a JSON"}), 400
    blob = request.get_json()
    """the state_id is not in database"""
    val = storage.get('Amenity', amenity_id)
    if val is None:
        abort(404)
    """because our api deals __class__,id, name, created_at,updated_at and we are to
    Ignore keys: id, created_at and updated_at"""
    val['name'] = blob['name']
    """to persist in storage"""
    val.save()
    return jsonify(val.to_dict())
