def test_home_page(app):
    response = app.get('/', headers={'api_token': 'token'})

    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the pet hotel"}


def test_check_in(app):
    room_id = 5
    name = 'Alex'

    response = app.post(
        '/check-in',
        json={
            "name": name,
            "phone": "123456789",
            "pets": {
                "Cat": [
                    {
                        "name": "Running",
                        "time": "8:00"
                    },
                    {
                        "name": "Walking",
                        "time": "19:30"
                    }
                ],
                "Dog": [
                    {
                        "name": "Running",
                        "time": "12:00"
                    },
                    {
                        "name": "Plyaing",
                        "time": "06:30"
                    }
                ]
            },
            "room_id": room_id
        },
        headers={'api_token': 'token'}
    )

    assert response.status_code == 200
    assert response.json == {"message": f"New owner {name} is checked-in with his pet(s)"}


def test_check_out(app):
    response = app.post(
        '/check-out',
        json={
            "pet_name": ['Cat', 'Dog'],
            "room_id": 5
        },
        headers={'api_token': 'token'}
    )

    assert response.status_code == 200
    assert response.json == {
        "Cat": "Lived days in hotel 0",
        "Dog": "Lived days in hotel 0"
    }


def test_activities(app):
    room_id = 5
    name = 'Alex'

    response = app.post(
        '/check-in',
        json={
            "name": name,
            "phone": "123456789",
            "pets": {
                "Cat": [
                    {
                        "name": "Running",
                        "time": "8:00"
                    },
                    {
                        "name": "Walking",
                        "time": "19:30"
                    }
                ],
                "Dog": [
                    {
                        "name": "Running",
                        "time": "12:00"
                    },
                    {
                        "name": "Plyaing",
                        "time": "06:30"
                    }
                ]
            },
            "room_id": room_id
        },
        headers={'api_token': 'token'}
    )

    assert response.status_code == 200
    assert response.json == {"status": "success"}

    response = app.get('/activities', headers={'api_token': 'token'})

    assert response.status_code == 200
    assert response.json == {
        "06:30": [
            {
                "pet_id": 77,
                "activity_type": "Plyaing"
            }
        ],
        "12:00": [
            {
                "pet_id": 77,
                "activity_type": "Running"
            }
        ],
        "19:30": [
            {
                "pet_id": 76,
                "activity_type": "Walking"
            }
        ],
        "8:00": [
            {
                "pet_id": 76,
                "activity_type": "Running"
            }
        ]
    }
