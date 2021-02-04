import datetime

import pytest
import psycopg2
from homework.sql_practice.crud_for_shop_db import DatabaseConnection


@pytest.fixture(scope='function')
def db_conn():
    db_conn = DatabaseConnection()
    yield db_conn
    db_conn.cursor.close()
    db_conn.conn.close()


class TestCasePositive:

    def test_crud_users(self, db_conn):
        new_user_info = {'name': 'Oleksandr', 'email': 'sasha@gmail.com', 'registration_time': '2021-02-03 12:40:00'}

        db_conn.create_user(new_user_info)
        user_id = db_conn.get_last_created_user_id()

        # updated value 'email'
        update_info_for_user = {'id': user_id, 'name': 'Oleksandr', 'email': 'oleksandr@gmail.com',
                                'registration_time': '2021-02-03 12:40:00'}

        assert db_conn.read_user_info(user_id) == (
            'Oleksandr', 'sasha@gmail.com', datetime.datetime(2021, 2, 3, 12, 40))

        db_conn.update_user(update_info_for_user)
        assert db_conn.read_user_info(user_id) == (
            'Oleksandr', 'oleksandr@gmail.com', datetime.datetime(2021, 2, 3, 12, 40))

        db_conn.delete_user(user_id)
        assert db_conn.read_user_info(user_id) is None

    def test_crud_cart(self, db_conn):
        # creating user for using his id in cart creation
        new_user_info = {'name': 'Oleksandr', 'email': 'sasha@gmail.com', 'registration_time': '2021-02-03 12:40:00'}
        db_conn.create_user(new_user_info)
        user_id = db_conn.get_last_created_user_id()

        new_cart = {'creation_time': '2000-02-04 11:20:00', 'user_id': user_id,
                    'cart_details': [{'price': 1000, 'product': 'Iphone'},
                                     {'price': 2000, 'product': 'Macbook'}]
                    }

        # creating cart
        db_conn.create_cart(new_cart)
        cart_id = db_conn.get_last_created_cart_id()

        # updated value creation_time
        update_info_for_cart = {'id': cart_id, 'creation_time': '2021-02-04 11:20:00', 'user_id': user_id}

        assert db_conn.read_cart(cart_id) == [(datetime.datetime(2000, 2, 4, 11, 20), 'Iphone', 1000),
                                              (datetime.datetime(2000, 2, 4, 11, 20), 'Macbook', 2000)]

        db_conn.update_cart(update_info_for_cart)
        assert db_conn.read_cart(cart_id) == [(datetime.datetime(2021, 2, 4, 11, 20), 'Iphone', 1000),
                                              (datetime.datetime(2021, 2, 4, 11, 20), 'Macbook', 2000)]

        # delete created data
        db_conn.delete_cart(cart_id)
        db_conn.delete_user(user_id)
        assert db_conn.read_cart(cart_id) == []


class TestCaseNegative:

    def test_crud_users(self, db_conn):
        # I use id - 999, as not existing
        not_exist_id = 999

        # user with existing name
        new_user_info = {'name': 'Alex', 'email': 'sasha@gmail.com', 'registration_time': '2021-02-03 12:40:00'}

        # updated value registration_time as not a datetime
        update_info_for_user = {'id': 2, 'name': 'Oleksandr', 'email': 'oleksandr@gmail.com',
                                'registration_time': 'not a datetime'}

        # error should be raised, when creating user on exiting name
        pytest.raises(psycopg2.Error, lambda: db_conn.create_user(new_user_info))

        # read_user_info() should return None, when passed id is not exist
        assert db_conn.read_user_info(not_exist_id) is None

        # error should be raised, when updating user with unexpected registration_time value
        pytest.raises(psycopg2.Error, lambda: db_conn.update_user(update_info_for_user))

        # delete_user() should return None, when passed id is not exist
        assert db_conn.delete_user(not_exist_id) is None

    def test_crud_cart(self, db_conn):
        # I use user_id - 999, as not existing
        not_exist_user_id = 999

        new_cart = {'creation_time': '2000-02-04 11:20:00', 'user_id': not_exist_user_id,
                    'cart_details': [{'price': 1000, 'product': 'Iphone'},
                                     {'price': 2000, 'product': 'Macbook'}]
                    }
        update_info_for_cart = {'id': 1, 'creation_time': '2021-02-04 11:20:00', 'user_id': not_exist_user_id}

        # creating cart on not existing user_id
        pytest.raises(psycopg2.Error, lambda: db_conn.create_cart(new_cart))

        # read_cart() should return [], when passed user_id is not exist
        assert db_conn.read_cart(not_exist_user_id) == []

        # error should be raised, when updating existing cart with not existing user_id value
        pytest.raises(psycopg2.Error, lambda: db_conn.update_cart(update_info_for_cart))

        # delete_cart() should return None, when passed id is not exist
        assert db_conn.delete_cart(not_exist_user_id) is None
