from datetime import datetime
from sqlalchemy.orm import backref
from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(240))
    role = db.Column(db.String(240), nullable=False)
    tickets = db.relationship('Ticket', backref='author', lazy=True)
    
    def __repr__(self):
        return f"User ('{self.username}', '{self.id}')"

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240), nullable=False)
    description = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Project( '{self.id}', '{self.title}'"

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(240), nullable=False)
    body = db.Column(db.Text())
    assigned_to = db.Column(db.String(240))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    high_priority = db.Column(db.Boolean)
    comments = db.Column(db.Text())
    status = db.Column(db.String(240), nullable=False)

    # def __repr__(self):
    #     return f"Ticket( '{self.id}', '{self.title}', '{self.assigned_to}'}')"
