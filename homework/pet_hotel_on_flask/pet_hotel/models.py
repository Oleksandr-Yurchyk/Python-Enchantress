from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    settlement_date = db.Column(db.DateTime)
    alias = db.Column(db.String)
    room_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))

    owner_info = db.relationship('Owner', backref='pet')


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    time = db.Column(db.String(10))
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))
