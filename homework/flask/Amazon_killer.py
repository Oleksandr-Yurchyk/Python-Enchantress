from flask import Flask, request
from datetime import datetime

amazon_killer = Flask(__name__)

USERS_DATABASE = {}
user_counter = 1
CART_DATABASE = {}
cart_counter = 1


class NoSuchCartError(Exception):
    def __init__(self, cart_id):
        self.cart_id = cart_id


class NoSuchUserError(Exception):
    def __init__(self, user_id):
        self.user_id = user_id


@amazon_killer.route('/users', methods=["POST"])
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


@amazon_killer.errorhandler(NoSuchUserError)
def no_such_user_handler(e):
    return {"error": f"no such user with id {e.user_id}"}, 404


@amazon_killer.route('/users/<int:user_id>')
def get_user(user_id):
    try:
        user = USERS_DATABASE[user_id]
    except KeyError:
        raise NoSuchUserError(user_id)
    else:
        return user


@amazon_killer.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    response = {"status": "success"}
    data_to_update = request.json
    try:
        user = USERS_DATABASE[user_id]

        user['name'] = data_to_update['name']
        user['email'] = data_to_update['email']

        USERS_DATABASE[user_id] = user
    except KeyError:
        raise NoSuchUserError(user_id)
    else:
        return response, 200


@amazon_killer.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    response = {"status": "success"}
    try:
        USERS_DATABASE.pop(user_id)
    except KeyError:
        raise NoSuchUserError(user_id)
    else:
        return response, 200


@amazon_killer.route('/carts', methods=['POST'])
def create_cart():
    global cart_counter

    cart = request.json
    response = {
        'cart_id': cart_counter,
        'creation_time': datetime.now().isoformat()
    }
    cart['cart_id'] = cart_counter
    cart['creation_time'] = response['creation_time']
    CART_DATABASE[cart_counter] = cart

    cart_counter += 1

    return response, 201


@amazon_killer.errorhandler(NoSuchCartError)
def cart_error_handler(e):
    return {'error': f'no such cart with id {e.cart_id}'}, 404


@amazon_killer.route('/carts/<int:cart_id>')
def get_cart(cart_id):
    try:
        cart = CART_DATABASE[cart_id]
    except KeyError:
        raise NoSuchCartError(cart_id)
    else:
        return cart


@amazon_killer.route('/carts/<int:cart_id>', methods=['PUT'])
def update_cart(cart_id):
    response = {'status': 'success'}
    data_to_update = request.json
    try:
        cart = CART_DATABASE[cart_id]

        cart['user_id'] = data_to_update['user_id']
        cart['products'] = data_to_update['products']

        CART_DATABASE[cart_id] = cart
    except KeyError:
        raise NoSuchCartError(cart_id)
    else:
        return response, 200


@amazon_killer.route('/carts/<int:cart_id>', methods=['DELETE'])
def delete_cart(cart_id):
    response = {"status": "success"}
    try:
        CART_DATABASE.pop(cart_id)
    except KeyError:
        raise NoSuchCartError(cart_id)
    else:
        return response, 200


if __name__ == '__main__':
    amazon_killer.run(debug=True)
