from datetime import datetime

from flask import Blueprint, request

user_bp = Blueprint('users', __name__)

USERS_DATABASE = {}
user_counter = 1
CART_DATABASE = {}
cart_counter = 1


class NoSuchUserError(Exception):
    def __init__(self, user_id):
        self.user_id = user_id


@user_bp.route('/users', methods=["POST"])
def create_user():
    global user_counter

    user = request.json
    response = {
        "registration_timestamp": datetime.now().isoformat(),
        "user_id": user_counter
    }
    user['user_id'] = user_counter
    user["registration_timestamp"] = response['registration_timestamp']

    USERS_DATABASE[user_counter] = user
    user_counter += 1

    return response, 201


@user_bp.errorhandler(NoSuchUserError)
def no_such_user_handler(e):
    return {"error": f"no such user with id {e.user_id}"}, 404


@user_bp.route('/users/<int:user_id>')
def get_user(user_id):
    user = USERS_DATABASE.get(user_id)
    if not user:
        raise NoSuchUserError(user_id)
    return user


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    response = {"status": "success"}
    data_to_update = request.json
    user = USERS_DATABASE.get(user_id)
    if user:
        user['name'] = data_to_update['name']
        user['email'] = data_to_update['email']

        USERS_DATABASE[user_id] = user
        return response, 200
    else:
        raise NoSuchUserError(user_id)


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    response = {"status": "success"}
    try:
        USERS_DATABASE.pop(user_id)
    except KeyError:
        raise NoSuchUserError(user_id)
    else:
        return response, 200
