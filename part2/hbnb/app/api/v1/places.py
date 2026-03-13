from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade


api = Namespace('places', description='Place operations')

# Models for related entities (for documentation, RESTX/SWAGGER)
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Input model
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})


def place_to_dict(place, include_owner=False, include_amenities=False, include_reviews=False):
    """Serialize a Place object to a dict."""
    data = {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
    }

    # owner_id in create response (as asked in example)
    if getattr(place, "owner", None) is not None:
        data["owner_id"] = place.owner.id

    if include_owner and getattr(place, "owner", None) is not None:
        o = place.owner
        data["owner"] = {
            "id": o.id,
            "first_name": o.first_name,
            "last_name": o.last_name,
            "email": o.email
        }

    if include_amenities:
        amenities = getattr(place, "amenities", []) or []
        data["amenities"] = [{"id": a.id, "name": a.name} for a in amenities]
    
    if include_reviews:
        reviews = getattr(place, "reviews", []) or []
        data["reviews"] = [
            {"id": r.id, "text": r.text, "rating": r.rating, "user_id": r.user.id}
        for r in reviews
        ]

    return data


@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = dict(api.payload)
        current_user = get_jwt_identity()

        place_data["owner_id"] = current_user

        try:
            new_place = facade.create_place(place_data)
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400

        return place_to_dict(new_place, include_owner=False, include_amenities=False), 201
    

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        # List response: light (example shows id, title, lat, lon)
        return [
            {
                "id": p.id,
                "title": p.title,
                "latitude": p.latitude,
                "longitude": p.longitude
            }
            for p in places
        ], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID (with owner and amenities)"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        return place_to_dict(place, include_owner=True, include_amenities=True, include_reviews=True), 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        if place.owner.id != current_user:
            return {"error": "Unauthorized action"}, 403

        place_data = dict(api.payload)
        place_data["owner_id"] = current_user

        try:
            updated = facade.update_place(place_id, place_data)
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400

        return place_to_dict(updated, include_owner=False, include_amenities=False), 200
    
#Nested endpoint to get reviews from specific place
@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {"error": "Place not found"}, 404

        return [
            {"id": r.id, "text": r.text, "rating": r.rating}
            for r in reviews
        ], 200