from flask import Blueprint, jsonify, request
from . import db
from .models import Ticket, User, Project
import bcrypt
main = Blueprint('main', __name__)

@main.route('/login', methods=['POST'])
def login():
    
    username = request.json.get('username')
    print(username)
    password = request.json.get('password')
    print(password)
    
    if not username: 
        return "Missing username", 401
    if not password:
        return "Missing password", 401

    user = User.query.filter_by(username=username).first()
    
    if not user:
        return "User not found", 404
    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        return "Welcome back " + username + "!!", 200
    else:
        return "Wrong Password!!", 401

@main.route('/add_project', methods=['POST'])
def add_project():
    project_data = request.get_json()
    new_project = Project(title=project_data['title'], description=project_data['description'],timestamp=project_data['timestamp'])

    db.session.add(new_project)
    db.session.commit()

    return 'Done', 201

@main.route('/add_ticket', methods=['POST'])
def add_ticket():
    ticket_data = request.get_json()
    print(ticket_data)
    new_ticket = Ticket(user_id=ticket_data['user_id'], title=ticket_data['title'], body=ticket_data['body'], assigned_to=ticket_data['assigned_to'], status=ticket_data['status'], comments=ticket_data['comments'], high_priority=ticket_data['high_priority'], timestamp=ticket_data['timestamp'])

    db.session.add(new_ticket)
    db.session.commit()

    return 'Done', 201

@main.route('/add_user', methods=['POST'])
def add_user():
    print("top of add_user")
    print(request)
    email = request.json.get('email')
    print(email)
    username = request.json.get('username', None)
    password = request.json.get('password1', None)
    # image_file = request.json.get('image_file', None)
    role = "user"

    if not email:
        return "Missing email", 400
    if not username: 
        return "Missing username", 400
    if not password:
        return "Missing password", 400

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    new_user = User(email=email, password=hashed_pw, username=username, role=role)

    db.session.add(new_user)
    db.session.commit()

    return 'Welcome, ' + username + '!!'
    # new_user = User(username=user_data['username'], password=user_data['password'], image_file=user_data['image_file'])

@main.route('/tickets')
def tickets():
    tickets_list = Ticket.query.all()
    tickets = []

    for ticket in tickets_list:
        tickets.append({'id': ticket.id, 'user_id': ticket.user_id, 'title': ticket.title, 'body': ticket.body, 'assigned_to': ticket.assigned_to, 'status': ticket.status, 'timestamp': ticket.timestamp, 'high_priority': ticket.high_priority, 'comments': ticket.comments})

    return jsonify({'tickets': tickets})

@main.route('/users')
def users():
    users_list = User.query.all()
    print(users_list)
    users = []

    for user in users_list:
        users.append({'username': user.username })
    print(users)
    return jsonify({'users': users})

@main.route('/user/<id>')
def user(id):
    user = User.query.filter_by(id=id).first()
    print(user)
    data = {"username": user.username}
    return jsonify(data)

@main.route('/ticket/<id>')
def ticket(id):
    ticket = Ticket.query.filter_by(id=id).first()
    data = {"user_id": ticket.user_id, "title": ticket.title, "body": ticket.body, "assigned_to": ticket.assigned_to, "status": ticket.status, "timestamp": ticket.timestamp, "comments": ticket.comments}
    return jsonify(data)

@main.route('/delete_ticket/<id>')
def delete_ticket(id):
    ticket = Ticket.query.filter_by(id=id).first()
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"response": "ticket deleted"}), 200

@main.route('/close_ticket/<id>', methods=['PUT'])
def close_ticket(id):
    ticket = Ticket.query.filter_by(id=id).first()
    print(ticket.status)
    # db.session.delete(ticket)
    ticket.status = "closed"
    db.session.commit()

    return jsonify({Ticket.status: "ticket closed"}), 200