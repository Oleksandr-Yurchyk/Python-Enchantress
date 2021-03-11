from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from .models import Order

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return jsonify({'home page status': 'success'}), 200


@main.route('/profile')
@login_required
def profile():
    user_id = current_user.id
    return jsonify({'profile page status': 'success',
                    'user_id': user_id}
                   ), 200


@main.route('/orders')
@login_required
def orders_list():
    user_id = current_user.id
    orders = Order.query.filter_by(user_id=user_id).all()

    return jsonify({'status': 'success',
                    'user_id': user_id,
                    'orders': orders}
                   ), 200
