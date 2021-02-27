from datetime import datetime

from flask import request
from flask_restful import Resource

USERS_DATABASE = {}
user_counter = 1
CART_DATABASE = {}
cart_counter = 1


class User(Resource):
    @classmethod
    def post(cls):
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

    @classmethod
    def get(cls, user_id):
        user = USERS_DATABASE.get(user_id)
        if not user:
            return {"error": f"no such user with id {user_id}"}, 404
        return user

    @classmethod
    def put(cls, user_id):
        response = {"status": "success"}
        data_to_update = request.json
        user = USERS_DATABASE.get(user_id)
        if user:
            user['name'] = data_to_update['name']
            user['email'] = data_to_update['email']

            USERS_DATABASE[user_id] = user
            return response, 200
        else:
            return {"error": f"no such user with id {user_id}"}, 404

    @classmethod
    def delete(cls, user_id):
        global user_counter

        response = {"status": "success"}
        try:
            USERS_DATABASE.pop(user_id)
        except KeyError:
            return {"error": f"no such user with id {user_id}"}, 404
        else:
            user_counter -= 1
            return response, 200


class Cart(Resource):
    @classmethod
    def post(cls):
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

    @classmethod
    def get(cls, cart_id):
        cart = CART_DATABASE.get(cart_id)
        if not cart:
            return {"error": f"no such cart with id {cart_id}"}, 404
        return cart

    @classmethod
    def put(cls, cart_id):
        response = {'status': 'success'}
        data_to_update = request.json
        cart = CART_DATABASE.get(cart_id)
        if cart:
            cart['user_id'] = data_to_update['user_id']
            cart['products'] = data_to_update['products']

            CART_DATABASE[cart_id] = cart
            return response, 200
        else:
            return {"error": f"no such cart with id {cart_id}"}, 404

    @classmethod
    def delete(cls, cart_id):
        global cart_counter

        response = {"status": "success"}
        try:
            CART_DATABASE.pop(cart_id)
        except KeyError:
            return {"error": f"no such cart with id {cart_id}"}, 404
        else:
            cart_counter -= 1
            return response, 200
