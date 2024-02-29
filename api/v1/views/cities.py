#!/usr/bin/python3
"""api module concearned with cities module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=['GET'])
def get_cities_in_a_state(state_id):
    """Retrieves the list of all State objects"""
    all_states = storage.get('State', state_id)
    if all_states is None:
        abort(404)
    values = [val.to_dict() for val in all_states.cities]
    return jsonify(values)


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """retrieves a state object"""
    value = storage.get('City', city_id)
    return jsonify(value.to_dict()) if value is not None else abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """deletes a city"""
    value = storage.get('City', city_id)
    abort(404) if value is None else value.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=['POST'])
def post_city(state_id):
    """posts data to existing json blob"""
    state_check = storage.get('State', state_id)
    if state_check is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error: Not a JSON"}), 400
    blob = request.get_json()
    if 'name' not in blob:
        return jsonify({"error: Missing name"}), 400
    """the form data might lack state_id which is a link to city"""
    blob['state_id'] = state_id
    """create it using the blob data"""
    newObject = City(**blob)
    """save it to persist in memory"""
    newObject.save()
    return jsonify(newObject.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def put_city(city_id):
    """updates City object"""
    if not request.get_json():
        return jsonify({"error: Not a JSON"}), 400
    blob = request.get_json()
    """the state_id is not in database"""
    val = storage.get('City', city_id)
    if val is None:
        abort(404)
    """because our api deals __class__,id, name, created_at,updated_at and we are to
    Ignore keys: id, created_at and updated_at"""
    val['name'] = blob['name']
    """to persist in storage"""
    val.save()
    return jsonify(val.to_dict())
