from flask import Flask
from flask_restful import Api

from homework.flask_2.restful_app.Amazon_killer_routes import User, Cart

amazon_killer = Flask(__name__)
api = Api(amazon_killer)

api.add_resource(User, '/users', '/users/<int:user_id>')
api.add_resource(Cart, '/carts', '/carts/<int:cart_id>')

if __name__ == '__main__':
    amazon_killer.run(debug=True)
