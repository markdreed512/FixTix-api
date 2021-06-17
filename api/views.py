from flask import Blueprint, jsonify, request
from . import db
from .models import Ticket, User

main = Blueprint('main', __name__)

@main.route('/add_ticket', methods=['POST'])
def add_ticket():
    ticket_data = request.get_json()
    print(ticket_data)
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
# @app.route('your route', methods=['GET'])
# def yourMethod(params):
#     response = flask.jsonify({'some': 'data'})
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response
@main.route('/tickets')
def tickets():
    tickets_list = Ticket.query.all()
    tickets = []

    for ticket in tickets_list:
        tickets.append({'id': ticket.id, 'user_id': ticket.user_id, 'title': ticket.title, 'body': ticket.body, 'assigned_to': ticket.assigned_to, 'completed': ticket.completed, 'timestamp': ticket.timestamp })

    return jsonify({'tickets': tickets})

@main.route('/ticket/<id>')
def ticket(id):
    ticket = Ticket.query.filter_by(id=id).first()
    data = {"user_id": ticket.user_id, "title": ticket.title, "body": ticket.body, "assigned_to": ticket.assigned_to, "completed": ticket.completed, "timestamp": ticket.timestamp}
    return jsonify(data)