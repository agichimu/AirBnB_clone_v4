#!/usr/bin/python3
"""api module concearned with cities module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'])
def get_users():
    """Retrieves the list of all User objects"""
    all_users = storage.all('User')
    values = [val.to_dict() for val in all_users.values()]
    return jsonify(values)


@app_views.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """retrieves a user object"""
    value = storage.get('User', user_id)
    return jsonify(value.to_dict()) if value is not None else abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """deletes a user"""
    value = storage.get('User', user_id)
    abort(404) if value is None else value.delete()
    storage.save()
    return jsonify({})


@app_views.route("/users", methods=['POST'])
def post_user():
    """posts data to existing json blob"""
    if not request.get_json():
        return jsonify({"error: Not a JSON"}), 400
    blob = request.get_json()
    if 'name' not in blob:
        return jsonify({"error: Missing name"}), 400
    """create it using the blob data"""
    newObject = User(**blob)
    """save it to persist in memory"""
    newObject.save()
    return jsonify(newObject.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def put_user(user_id):
    """updates a User object"""
    if not request.get_json():
        return jsonify({"error: Not a JSON"}), 400
    blob = request.get_json()
    """the state_id is not in database"""
    val = storage.get('User', user_id)
    if val is None:
        abort(404)
    """because our api deals __class__,id, name, created_at,updated_at and we are to
    Ignore keys: id, created_at and updated_at"""
    val['name'] = blob['name']
    """to persist in storage"""
    val.save()
    return jsonify(val.to_dict())
