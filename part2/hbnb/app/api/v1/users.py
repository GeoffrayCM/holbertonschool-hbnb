from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


@api.route('/')
class UserList(Resource):
    """ Userlist = collection of users """
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        # create a copy of payload to store then escape password
        user_data = dict(api.payload)

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        # get password value and remove it from dict to separate it from the rest (userdata to create user without psswd)
        password = user_data.pop('password')

        try :
            new_user = facade.create_user(user_data)
            # call hash method apart from create user
            new_user.hash_password(password)
        except ValueError as e:
            return {"error": str(e)}, 400
        return {'id': new_user.id, 'message': 'User successfully created'}, 201
    
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """ get users list"""
        users = facade.get_users()
        return [{"id": u.id, "first_name": u.first_name, "last_name": u.last_name, "email": u.email}
                for u in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    """ UserResource = a precise element from a user """
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update User information"""
        user_data = api.payload

        update_user = facade.update_user(user_id, user_data)
        if not update_user:
            return {'error': 'User not found'}, 404
        
        return {
            "id": update_user.id,
            "first_name": update_user.first_name,
            "last_name": update_user.last_name,
            "email": update_user.email
        }, 200
    
    
