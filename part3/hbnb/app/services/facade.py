from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)

    # Create admin directly for testing
    def _seed_admin_user(self):
        """Create a default admin user for testing."""
        existing_admin = self.user_repo.get_by_attribute("email", "admin@hbnb.io")
        if existing_admin:
            return

        admin = User(
            first_name="Admin",
            last_name="HBnB",
            email="admin@hbnb.io",
            is_admin=True
        )
        admin.hash_password("admin1234")
        self.user_repo.add(admin)

    # USER METHODS
    def create_user(self, user_data):
        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            is_admin=user_data.get("is_admin", False)
        )

        user.hash_password(user_data["password"])

        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)
    
    def get_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        #update method from model user
        user.update(user_data)
        return user

    # AMENITY METHODS
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)  # appelle Amenity.update() + save()
        return amenity
    
    # PLACE METHODS
    def create_place(self, place_data):
        owner = self.user_repo.get(place_data.get("owner_id"))
        if not owner:
            raise ValueError("Invalid owner_id")
        
        place = Place(
            title=place_data.get("title"),
            description=place_data.get("description"),
            price=place_data.get("price"),
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            user_id=owner.id
        )
        if "amenities" in place_data:
            for amenity_id in place_data["amenities"]:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError("Invalid amenity_id")
                place.amenities.append(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        if "owner_id" in place_data:
            owner = self.user_repo.get(place_data["owner_id"])
            if not owner:
                raise ValueError("Invalid owner_id")
            place_data = dict(place_data)
            place_data["user_id"] = owner.id
            del place_data["owner_id"]

        if "amenities" in place_data:
            new_amenities = []
            for amenity_id in place_data["amenities"]:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError("Invalid amenity_id")
                new_amenities.append(amenity)

            place.amenities = new_amenities

            place_data = dict(place_data)
            del place_data["amenities"]

        place.update(place_data)
        return place
    
    # REVIEW METHODS
    def create_review(self, review_data):
        place = self.place_repo.get(review_data.get("place_id"))
        if not place:
            raise ValueError("Invalid place_id")
        
        user = self.user_repo.get(review_data.get("user_id"))
        if not user:
            raise ValueError("Invalid user_id")

        review = Review(
            text=review_data.get("text"),
            rating=review_data.get("rating"),
            place_id=place.id,
            user_id=user.id
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None  # API will return 404
        return getattr(place, "reviews", []) or []


    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        # Don't allow changing relations
        if "user_id" in review_data or "place_id" in review_data:
            raise ValueError("Cannot update user_id or place_id")

        review.update(review_data)
        return review

    # Simplified with SQL alch
    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False

        self.review_repo.delete(review_id)
        return True
