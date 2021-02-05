import psycopg2


class DatabaseConnection:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname='olexandr_yurchyk',
                user='olexandr_yurchyk',
                password=111,
                host='localhost'
            )
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
        except (Exception, psycopg2.Error) as error:
            print('Oops.. some error occurs during connecting to DB \n', error)

    def create_user(self, user_info: dict):
        create_user_query = """
        INSERT INTO users (name, email, registration_time)
        VALUES (%(name)s, %(email)s, %(registration_time)s);
        """
        self.cursor.execute(create_user_query, user_info)

    def get_last_created_user_id(self):
        last_created_user_query = """
        SELECT id, name FROM users
        ORDER BY id DESC LIMIT 1;
        """
        self.cursor.execute(last_created_user_query)
        id, name = self.cursor.fetchone()
        return id

    def read_user_info(self, _id: int):
        read_user_info_query = """
        SELECT name, email, registration_time FROM users
        WHERE id = %s;
        """
        self.cursor.execute(read_user_info_query, (_id,))
        user = self.cursor.fetchone()
        print(user)
        return user

    def update_user(self, new_info: dict):
        update_user_query = """
        UPDATE users
        SET name=%(name)s, email=%(email)s, registration_time=%(registration_time)s
        WHERE id = %(id)s;
        """
        self.cursor.execute(update_user_query, new_info)

    def delete_user(self, _id: int):
        delete_user_query = """
        DELETE FROM users
        WHERE id = %s;
        """
        self.cursor.execute(delete_user_query, (_id,))

    def create_cart(self, cart: dict):
        create_cart_query = """
        INSERT INTO cart (creation_time, user_id)
        VALUES (%(creation_time)s, %(user_id)s);
        """
        self.cursor.execute(create_cart_query, cart)

        cart_id = self.get_last_created_cart_id()

        create_cart_details_query = f"""
        INSERT INTO cart_details (cart_id, price, product)
        VALUES ({cart_id}, %(price)s, %(product)s);
        """
        self.cursor.executemany(create_cart_details_query, cart.get('cart_details'))

    def get_last_created_cart_id(self):
        last_created_cart_query = """
        SELECT id, creation_time FROM cart
        ORDER BY id DESC LIMIT 1;
        """
        self.cursor.execute(last_created_cart_query)
        id, creation_time = self.cursor.fetchone()
        return id

    def read_cart(self, _id: int):
        read_cart_and_its_details_query = """
        SELECT cart.creation_time AS cart_creation_time, cd.product, cd.price 
        FROM cart LEFT JOIN cart_details AS cd 
        ON cd.cart_id=cart.id
        WHERE cart.id=%s;
        """
        self.cursor.execute(read_cart_and_its_details_query, (_id,))
        cart = self.cursor.fetchall()
        print(cart)
        return cart

    def update_cart(self, cart: dict):
        update_cart_query = """
        UPDATE cart
        SET creation_time=%(creation_time)s, user_id=%(user_id)s
        WHERE id=%(id)s
        """
        self.cursor.execute(update_cart_query, cart)

        update_cart_details_query = """
        UPDATE cart_details
        SET price=%(price)s, product=%(product)s
        WHERE cart_id=%(cart_id)s
        """
        self.cursor.executemany(update_cart_details_query, cart.get('cart_details'))

    def delete_cart(self, _id: int):
        delete_cart_details_query = """
        DELETE FROM cart_details
        WHERE cart_id=%s
        """
        self.cursor.execute(delete_cart_details_query, (_id,))

        delete_cart_query = """
        DELETE FROM cart
        WHERE id=%s
        """
        self.cursor.execute(delete_cart_query, (_id,))
