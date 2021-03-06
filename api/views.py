from flask import Blueprint, jsonify, request
from . import db
from .models import Ticket, User, Project
import bcrypt
main = Blueprint('main', __name__)

@main.route('/login', methods=['POST'])
def login():
    
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username: 
        return "Missing username", 401
    if not password:
        return "Missing password", 401

    user = User.query.filter_by(username=username).first()
    
    if not user:
        return "User not found", 404
    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        # should return user object here:
        data = {"username": user.username, "id": user.id }
        return jsonify(data)
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
    new_ticket = Ticket(user_id=ticket_data['user_id'], title=ticket_data['title'], body=ticket_data['body'], assigned_to=ticket_data['assigned_to'], status=ticket_data['status'], comments=ticket_data['comments'], high_priority=ticket_data['high_priority'], timestamp=ticket_data['timestamp'])

    db.session.add(new_ticket)
    db.session.commit()

    return 'Ticket Added', 201

@main.route('/add_user', methods=['POST'])
def add_user():
    email = request.json.get('email')
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

@main.route('/projects')
def projects():
    projects_list = Project.query.all()
    projects = []

    for project in projects_list:
        projects.append({'title': project.title, 'description': project.description, 'timestamp': project.timestamp})

    return jsonify(projects)

@main.route('/users')
def users():
    users_list = User.query.all()
    users = []

    for user in users_list:
        users.append({'username': user.username })
    return jsonify({'users': users})

@main.route('/user/<id>')
def user(id):
    user = User.query.filter_by(id=id).first()
    data = {"username": user.username}
    return jsonify(data)

@main.route('/ticket/<id>')
def ticket(id):
    ticket = Ticket.query.filter_by(id=id).first()
    data = {"id": ticket.id, "user_id": ticket.user_id, "title": ticket.title, "description": ticket.body, "assigned_to": ticket.assigned_to, "status": ticket.status, "timestamp": ticket.timestamp, "comments": ticket.comments, "high_priority": ticket.high_priority}
    return jsonify(data)

@main.route('/tickets/<id>')
def mytickets(id):
    print("Yoo...hO000....")
    tickets = Ticket.query.filter_by(user_id=id).all()
    print(tickets)
    # iterate over tickets, pull out each property, stick it into an obj, and push obj to array
    ticket_list = []
    for ticket in tickets:
        data = {"id": ticket.id, "user_id": ticket.user_id, "title": ticket.title, "description": ticket.body, "assigned_to": ticket.assigned_to, "status": ticket.status, "timestamp": ticket.timestamp, "comments": ticket.comments, "high_priority": ticket.high_priority}
        ticket_list.append(data)

    return jsonify(ticket_list)

@main.route('/delete_ticket/<id>')
def delete_ticket(id):
    ticket = Ticket.query.filter_by(id=id).first()
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"response": "ticket deleted"}), 200

@main.route('/close_ticket/<id>', methods=['PUT'])
def close_ticket(id):
    ticket = Ticket.query.filter_by(id=id).first()
    ticket.status = "closed"
    db.session.commit()

    return jsonify({Ticket.status: "ticket closed"}), 200

@main.route('/edit_ticket/<id>', methods=['GET', 'PUT'])
def edit_ticket(id):
    ticket = Ticket.query.filter_by(id=id).first()
    request_data = request.get_json()
    print("request body: ") 
    print(request_data)
    ticket.title = request_data['title']
    ticket.body = request_data['body']
    ticket.assigned_to = request_data['assigned_to']
    ticket.high_priority = request_data['high_priority']
    ticket.comments = request_data['comments']
    db.session.commit()

    return "done."