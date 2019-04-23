from app import app, db
from flask import Flask, request, jsonify, json, render_template
from app.models import User, Event, Pet
from datetime import datetime
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)
from app.email import send_email

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)


# set index route to return nothing, just so no error occurs
@app.route('/')
def index():
    return ''


@app.route('/api/register', methods=['GET', 'POST'])
def register():
    # try:
    first_name = request.headers.get('first_name')
    last_name = request.headers.get('last_name')
    street = request.headers.get('street')
    city = request.headers.get('city')
    state = request.headers.get('state')
    zip = request.headers.get('zip')
    phone = request.headers.get('phone')
    email = request.headers.get('email')
    password = request.headers.get('password')

    password = bcrypt.generate_password_hash(password).decode('utf-8')

    # if not all exist, return error
    if not first_name and not last_name and not email:
        return jsonify({ 'error': 'Invalid params' })

    # create a user
    user = User(first_name=first_name, last_name=last_name, street=street, city=city, state=state, zip=zip, phone=phone, email=email, password=password)

    # add and commit to db
    db.session.add(user)
    db.session.commit()

    return jsonify({ 'success': 'Saved user' })

    # except:
        # return jsonify({ 'error': 'invalid params, did not save' })

@app.route('/api/retrieve', methods=['GET', 'POST'])
def retrieve():
    try:
        first_name = request.headers.get('first_name')
        last_name = request.headers.get('last_name')
        street = request.headers.get('street')
        city = request.headers.get('city')
        state = request.headers.get('state')
        zip = request.headers.get('zip')
        phone = request.headers.get('phone')
        email = request.headers.get('email')
        # password = request.headers.get('password')

        results = User.query.all()

        users = []

        # loop through results and add each user to list
        for result in results:
            user = {
                'id': result.id,
                'first_name': result.first_name,
                'last_name': result.last_name,
                'street': result.street,
                'city': result.city,
                'state': result.state,
                'zip': result.zip,
                'phone': result.phone,
                'email': result.email
            }

            users.append(user)

        return jsonify(users)

    except:
        return jsonify([])

@app.route('/api/delete', methods=['GET', 'POST'])
def delete():
    try:
        id = request.headers.get('id')

        user = User.query.filter_by(id=id).first()

        db.session.delete(user)
        db.session.commit()

        return jsonify({ 'success': 'User deleted' })

    except:
        return jsonify({ 'error': 'User not removed, try again' })

@app.route('/api/save', methods=['GET', 'POST'])
def save():
    try:
        user_id = request.headers.get('user_id')
        service = request.headers.get('service')
        day = request.headers.get('day')
        month = request.headers.get('month')
        year = request.headers.get('year')
        hours = request.headers.get('hours')
        minutes = request.headers.get('minutes')
        notes = request.headers.get('notes')
        pet = request.headers.get('pet')
        duration = request.headers.get('duration')

        # query database to see if time available then save if you can, or return error

        # if not all exist, return error
        if not day and not month and not year and not service:
            return jsonify({ 'error': 'Invalid params' })

        # if day, month, year, hours, minutes already exists, return error


        # create an event
        event = Event(user_id=user_id, service=service, day=day, month=month, year=year, hours=hours, minutes=minutes, notes=notes, pet=pet, duration=duration)

        # add and commit to db
        db.session.add(event)
        db.session.commit()

        # call email

        id = Event.user_id

        user = User.query.filter_by(id=id).first()

        send_email(
        subject = "Your Kett's Pets Appointment",
        sender = app.config['ADMINS'][0],
        recipients = [user.email],
        text_body = render_template('email/appt.txt',
            name = user.first_name,
            pet = Event.pet,
            service = Event.service),
        html_body = render_template('email/appt.html',
            name = user.first_name,
            pet = Event.pet,
            service = Event.service)
    )

        return jsonify({ 'success': 'Saved event' })

    except:
        return jsonify({ 'error': 'invalid params, did not save' })

@app.route('/api/retrieve_event', methods=['GET', 'POST'])
def retrieveEvent():
    try:
        event_id = request.headers.get('event_id')
        user_id = request.headers.get('user_id')
        service = request.headers.get('service')
        day = request.headers.get('day')
        month = request.headers.get('month')
        year = request.headers.get('year')
        hours = request.headers.get('hours')
        minutes = request.headers.get('minutes')
        notes = request.headers.get('notes')
        pet = request.headers.get('pet')
        duration = request.headers.get('duration')


        if not day and month and year:
            results = Event.query.filter_by(month=month, year=year).all()
        elif not day and not month and year:
            results = Event.query.filter_by(year=year).all()
        else:
            results = Event.query.filter_by(year=year, month=month, day=day).all()

        if results == []:
            return jsonify({ 'success': 'No events today' })

        appointments = []

        for result in results:
            appointment = {
                'user_id': result.user_id,
                'service': result.service,
                'day': result.day,
                'month': result.month,
                'year': result.year,
                'hours': result.hours,
                'minutes': result.minutes,
                'notes': result.notes,
                'event_id': result.event_id
            }

            appointments.append(appointment)

        return jsonify(appointments)

    except:
        return jsonify([])

@app.route('/api/delete_event', methods=['GET', 'POST'])
def deleteEvent():
    try:
        event_id = request.headers.get('event_id')

        event = Event.query.filter_by(event_id=event_id).first()

        db.session.delete(event)
        db.session.commit()

        return jsonify({ 'success': 'Event deleted' })

    except:
        return jsonify({ 'error': 'Event not removed, try again' })

@app.route('/api/save_pet', methods=['GET', 'POST'])
def savePet():
    try:
        pet_name = request.headers.get('pet_name')
        user_id = request.headers.get('user_id')

        if not pet_name:
            return jsonify({ 'error': 'Invalid params' })

        # create a pet
        pet = Pet(pet_name=pet_name, user_id=user_id)

        # add and commit to db
        db.session.add(pet)
        db.session.commit()

        return jsonify({ 'success': 'Saved pet', 'pet_name': pet.pet_name })

    except:
        return jsonify({ 'error': 'invalid params, did not save' })

@app.route('/api/retrieve_pets', methods=['GET', 'POST'])
def retrievePets():
    try:
        pet_id = request.headers.get('pet_id')
        pet_name = request.headers.get('pet_name')
        user_id = request.headers.get('user_id')

        results = Pet.query.all()

        if results == []:
            return jsonify({ 'success': 'No Pets' })

        pets = []

        # loop through results and add each pet to pets list
        for result in results:
            pet = {
                'pet_id': result.pet_id,
                'pet_name': result.pet_name,
                'user_id': result.user_id
            }

            pets.append(pet)

        return jsonify(pets)

    except:
        return jsonify([])

@app.route('/api/delete_pet', methods=['GET', 'POST'])
def deletePet():
    try:
        pet_id = request.headers.get('pet_id')

        pet = Pet.query.filter_by(pet_id=pet_id).first()

        db.session.delete(pet)
        db.session.commit()

        return jsonify({ 'success': 'Pet deleted' })

    except:
        return jsonify({ 'error': 'Pet not removed, try again' })

@app.route('/api/login', methods=['GET', 'POST'])
def login():

    email = request.headers.get('email')
    password = request.headers.get('password')
    result = ''

    res = User.query.filter_by(email=email).first()

    try:
        if bcrypt.check_password_hash(res.password, password):
            # access_token = create_access_token(identity = {'first_name': res.first_name, 'last_name': res.last_name, 'email': res.email})
            # result = access_token
            result = jsonify({
                'success': 'You are now logged in.',
                'user_id': res.id,
                'first_name': res.first_name,
                'last_name': res.last_name,
                'street': res.street,
                'city': res.city,
                'state': res.state,
                'zip': res.zip,
                'phone': res.phone,
                'email': res.email,
            })
        else:
            result = jsonify({'error':'Invalid username and password'})

    except:
        return jsonify({ 'error': 'Not able to login' })

    return result
