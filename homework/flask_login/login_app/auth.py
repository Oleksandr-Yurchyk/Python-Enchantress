from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return jsonify({'login page status': 'success'}), 200


@auth.route('/signup')
def signup():
    return jsonify({'signup page status': 'success'}), 200


@auth.route('/logout')
@login_required
def logout():
    user_id = current_user.id
    logout_user()
    return jsonify({'message': f'user {user_id} logout successfully'}), 200


@auth.route('/signup', methods=['POST'])
def signup_post():
    terminal_request = """
    curl -i -X POST -H 'Content-Type:application/json' -d '{"name":"admin","email":"admin@admin.com","password":"pass"}' 
    http://127.0.0.1:5000/signup
    """
    body = request.get_json()
    email = body['email']
    name = body['name']
    password = body['password']

    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({'error': f'user with {user.email} email already exist'}), 409

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': f'user {new_user.name} created successfully'}), 200


@auth.route('/login', methods=['POST'])
def login_post():
    if current_user.is_authenticated:
        return jsonify({'message': f'user {current_user.name} already logged in'})

    terminal_request = """
    curl -i -X POST -H 'Content-Type:application/json' -d '{"email":"user","password":"user","remember":"True"}'
    http://127.0.0.1:5000/login
    """
    body = request.get_json()
    email = body['email']
    password = body['password']
    remember = True if body['remember'] else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Email or password invalid'}), 401

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    # session[]
    return jsonify(
        {'message': 'user logged in successfully',
         'user_id': user.id,
         'user_email': user.email}
    ), 200
