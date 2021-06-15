from flask import Blueprint, jsonify, request
from . import db
from .models import Ticket, User

main = Blueprint('main', __name__)

@main.route('/add_ticket', methods=['POST'])
def add_ticket():
    ticket_data = request.get_json()

    new_ticket = Ticket(user_id=ticket_data['user_id'], title=ticket_data['title'], body=ticket_data['body'], assigned_to=ticket_data['assigned_to'], completed=ticket_data['completed'],timestamp=ticket_data['timestamp'])

    db.session.add(new_ticket)
    db.session.commit()

    return 'Done', 201

@main.route('/add_user', methods=['POST'])
def add_user():
    user_data = request.get_json()
    new_user = User(username=user_data['username'], password=user_data['password'], image_file=user_data['image_file'])

    db.session.add(new_user)
    db.session.commit()

    return 'Done', 201

@main.route('/tickets')
def tickets():

    tickets = []

    return jsonify({'tickets': tickets})