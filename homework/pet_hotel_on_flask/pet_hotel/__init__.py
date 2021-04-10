from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from .config import Config
from .middleware import APIMiddleware
from .models import db


def create_app():
    app = Flask(__name__)
    app.wsgi_app = APIMiddleware(app.wsgi_app)
    api = Api(app=app)

    app.config.from_object(Config())
    db.init_app(app)
    migrate = Migrate(app, db)

    from .routes import HomePage, RoomPage, CheckInPage, CheckOutPage, ActivityPage
    api.add_resource(HomePage, '/')
    api.add_resource(RoomPage, '/room/<int:room_id>')
    api.add_resource(CheckInPage, '/check-in')
    api.add_resource(CheckOutPage, '/check-out')
    api.add_resource(ActivityPage, '/activities')

    @app.cli.command('create-db')
    def create_db():
        db.drop_all()
        db.create_all()

    return app
