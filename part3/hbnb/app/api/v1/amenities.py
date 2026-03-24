from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.api.v1.auth_utils import is_admin
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    """ Collection of amenitys """
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new amenity (admin only)"""
        if not is_admin():
            return {"error": "Admin privileges required"}, 403
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError as e:
            return {"error": str(e)}, 400
        return {"id": new_amenity.id, "name": new_amenity.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{"id": a.id, "name": a.name} for a in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """ Precise element """
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return {"id": amenity.id, "name": amenity.name}, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        if not is_admin():
            return {"error": "Admin privileges required"}, 403
        
        amenity_data = api.payload
        try:
            updated = facade.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            return {"error": str(e)}, 400
        if not updated:
            return {"error": "Amenity not found"}, 404
        return {"id": updated.id, "name": updated.name}, 200
