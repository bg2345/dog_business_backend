from app import app, db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    street = db.Column(db.String(64))
    city = db.Column(db.String(50))
    state = db.Column(db.String(25))
    zip = db.Column(db.String(15))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    events = db.relationship('Event', backref=db.backref('user', lazy='joined'))
    pet = db.relationship('Pet', backref=db.backref('user', lazy='joined'))

    def __repr__(self):
        return '<User {}>'.format(self.email)

class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service = db.Column(db.String(50))
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    hours = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    notes = db.Column(db.String(500))

class Pet(db.Model):
    pet_id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
