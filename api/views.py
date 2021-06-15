from flask import Blueprint, jsonify, request
from . import db
from .models import Ticket, User

main = Blueprint('main', __name__)

@main.route('/add_ticket', methods=['POST'])
def add_ticket():
    ticket_data = request.get_json()

    new_ticket = Ticket(ticket_data['user_id'], ticket_data['password'], ticket_data['title'], ticket_data['body'], ticket_data['assigned_to'], ticket_data['completed'],ticket_data['timestamp'])

    db.session.add(new_ticket)
    db.session.commit()

    return 'Done', 201

@main.route('/add_user', methods=['POST'])
def add_user():
    print("hellooooo.........")
    user_data = request.get_json()
    print(user_data)
    new_user = User(username=user_data['username'], password=user_data['password'], image_file=user_data['image_file'])
# create_post = Post(title=my_form.title.data, text=my_form.text.data)
    db.session.add(new_user)
    db.session.commit()

    return 'Done', 201

@main.route('/tickets')
def tickets():

    tickets = []

    return jsonify({'tickets': tickets})