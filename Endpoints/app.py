from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from datetime import datetime

app = Flask(__name__)
api = Api(app, version='1.0', title='User API',
          description='A simple User API',
          )

ns = api.namespace('users', description='User operations')

# Define the user model for the API documentation
user_model = api.model('User', {
    'id': fields.String(readonly=True, description='The user unique identifier'),
    'email': fields.String(required=True, description='The user email address'),
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(required=True, description='The user last name'),
    'created_at': fields.String(readonly=True, description='The user creation date'),
    'updated_at': fields.String(readonly=True, description='The user update date')
})

# In-memory storage for users
users = {}
user_counter = 1

def validate_email(email):
    if '@' not in email or '.' not in email.split('@')[-1]:
        return False
    return True

def serialize_datetime(dt):
    if dt:
        return dt.isoformat()
    return None

@ns.route('/')
class UserList(Resource):
    @ns.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        return [serialize_user(user) for user in users.values()], 200

    @ns.expect(user_model)
    @ns.response(201, 'User created successfully')
    @ns.response(400, 'Bad Request')
    @ns.response(409, 'Conflict')
    def post(self):
        """Create a new user"""
        global user_counter
        data = request.json
        email = data.get('email')

        if not validate_email(email):
            api.abort(400, "Invalid email format")
        
        if email in [user['email'] for user in users.values()]:
            api.abort(409, "Email already exists")

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if not first_name or not last_name:
            api.abort(400, "First name and last name cannot be empty")

        user_id = str(user_counter)
        user_counter += 1
        new_user = {
            'id': user_id,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        users[user_id] = new_user
        return serialize_user(new_user), 201


@ns.route('/<string:user_id>')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class User(Resource):
    @ns.marshal_with(user_model)
    def get(self, user_id):
        """Fetch a user given its identifier"""
        if user_id not in users:
            api.abort(404, "User not found")
        return serialize_user(users[user_id]), 200

    @ns.expect(user_model)
    @ns.response(200, 'User updated successfully')
    @ns.response(400, 'Bad Request')
    @ns.response(404, 'User not found')
    @ns.response(409, 'Conflict')
    def put(self, user_id):
        """Update a user given its identifier"""
        if user_id not in users:
            api.abort(404, "User not found")

        data = request.json
        email = data.get('email')

        if not validate_email(email):
            api.abort(400, "Invalid email format")
        
        if email in [user['email'] for user in users.values() if user['id'] != user_id]:
            api.abort(409, "Email already exists")

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if not first_name or not last_name:
            api.abort(400, "First name and last name cannot be empty")

        users[user_id].update({
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'updated_at': datetime.utcnow()
        })
        return serialize_user(users[user_id]), 200

    @ns.response(204, 'User deleted successfully')
    def delete(self, user_id):
        """Delete a user given its identifier"""
        if user_id not in users:
            api.abort(404, "User not found")
        del users[user_id]
        return '', 204

def serialize_user(user):
    return {
        'id': user['id'],
        'email': user['email'],
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'created_at': serialize_datetime(user['created_at']),
        'updated_at': serialize_datetime(user['updated_at'])
    }

if __name__ == '__main__':
    app.run(debug=True)
