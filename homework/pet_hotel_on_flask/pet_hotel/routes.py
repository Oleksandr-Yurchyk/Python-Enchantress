import datetime
from flask import request
from flask_restful import Resource

from pet_hotel.models import Owner, db, Pet, Activity


class HomePage(Resource):
    def get(self):
        return {"message": "Welcome to the pet hotel"}, 200


class RoomPage(Resource):
    def get(self, room_id):
        settlers = Pet.query.filter_by(room_id=room_id).all()
        pets = {}
        for settler in settlers:
            pets[settler.alias] = f'pet_id: {settler.id}, ' \
                                  f'owner: {settler.owner_info.name}, ' \
                                  f'settlement_date: {settler.settlement_date}'
        if pets:
            return pets, 200
        else:
            return {'message': 'room is empty'}, 200


class CheckInPage(Resource):
    def post(self):
        response = request.get_json()
        name = response.get('name')
        phone = response.get('phone')
        pets = response.get('pets')
        room_id = response.get('room_id')

        new_owner = Owner(name=name, phone=phone)

        db.session.add(new_owner)
        db.session.commit()

        pets_name = []
        for pet_name in pets:
            new_pet = Pet(alias=pet_name,
                          owner_id=new_owner.id,
                          room_id=room_id,
                          settlement_date=datetime.datetime.now())
            pets_name.append(pet_name)

            db.session.add(new_pet)
            db.session.commit()

            for activity in pets.get(pet_name):
                pet_activity = Activity(type=activity.get('name'),
                                        time=activity.get('time'),
                                        pet_id=new_pet.id)
                db.session.add(pet_activity)
                db.session.commit()

        return {"message": f"New owner {new_owner.name} is checked-in with his pet(s)"}, 200


class CheckOutPage(Resource):
    def post(self):
        response = request.get_json()
        pet_names = response['pet_name']
        room_id = response['room_id']

        response = {}
        for pet_name in pet_names:
            pet = Pet.query.filter_by(alias=pet_name, room_id=room_id).first()
            pet_activities = Activity.query.filter_by(pet_id=pet.id).all()

            lived_days = (datetime.datetime.now() - pet.settlement_date).days

            for activity in pet_activities:
                db.session.delete(activity)
            db.session.commit()
            db.session.delete(pet)
            db.session.commit()

            if Pet.query.filter_by(alias=pet_name, room_id=room_id).first() is None:
                owner = Owner.query.filter_by(id=pet.owner_id).first()
                db.session.delete(owner)
                db.session.commit()

            response[pet_name] = f"Lived days in hotel {lived_days}"
        return response, 200


class ActivityPage(Resource):
    def get(self):
        information = {}
        activities_list = Activity.query.all()

        for activity in activities_list:
            if activity.time not in information:
                information[activity.time] = []
            information[activity.time].append({'pet_id': activity.pet_id, 'activity_type': activity.type})

        response = {}
        for key in sorted(information):
            response[key] = information[key]

        return response
