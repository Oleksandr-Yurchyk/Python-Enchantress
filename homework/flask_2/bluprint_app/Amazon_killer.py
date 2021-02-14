from flask import Flask

from homework.flask_2.bluprint_app.cart.cart import cart_bp
from homework.flask_2.bluprint_app.user.user import user_bp

amazon_killer = Flask(__name__)
amazon_killer.register_blueprint(user_bp)
amazon_killer.register_blueprint(cart_bp)

if __name__ == '__main__':
    amazon_killer.run(debug=True)
