from datetime import datetime

from flask import Blueprint, request

cart_bp = Blueprint('carts', __name__)

CART_DATABASE = {}
cart_counter = 1


class NoSuchCartError(Exception):
    def __init__(self, cart_id):
        self.cart_id = cart_id


@cart_bp.route('/carts', methods=['POST'])
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


@cart_bp.errorhandler(NoSuchCartError)
def cart_error_handler(e):
    return {'error': f'no such cart with id {e.cart_id}'}, 404


@cart_bp.route('/carts/<int:cart_id>')
def get_cart(cart_id):
    cart = CART_DATABASE.get(cart_id)
    if not cart:
        raise NoSuchCartError(cart_id)
    return cart


@cart_bp.route('/carts/<int:cart_id>', methods=['PUT'])
def update_cart(cart_id):
    response = {'status': 'success'}
    data_to_update = request.json
    cart = CART_DATABASE.get(cart_id)
    if cart:
        cart['user_id'] = data_to_update['user_id']
        cart['products'] = data_to_update['products']

        CART_DATABASE[cart_id] = cart
        return response, 200
    else:
        raise NoSuchCartError(cart_id)


@cart_bp.route('/carts/<int:cart_id>', methods=['DELETE'])
def delete_cart(cart_id):
    response = {"status": "success"}
    try:
        CART_DATABASE.pop(cart_id)
    except KeyError:
        raise NoSuchCartError(cart_id)
    else:
        return response, 200
