from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
    # USER METHODS
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
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
        amenity = Amenity(**amenity_data)  # amenity_data = {"name": "..."}
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
          # 1) owner
        owner_id = place_data.get("owner_id")
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Invalid owner_id")

            # 2) amenities IDs -> objects
        amenities_ids = place_data.get("amenities", [])
        amenities = []
        for amenity_id in amenities_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError("Invalid amenity_id")
            amenities.append(amenity)

            # 3) Create place (owner object, not owner_id)
        new_place = Place(
            title=place_data.get("title"),
            description=place_data.get("description"),
            price=place_data.get("price"),
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            owner=owner
        )

        # 4) Attach amenities (no reviews here)
        for a in amenities:
            new_place.add_amenity(a)

        # 5) store
        self.place_repo.add(new_place)
        return new_place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # If owner_id provided, validate and convert to owner object
        if "owner_id" in place_data:
            owner = self.user_repo.get(place_data["owner_id"])
            if not owner:
                raise ValueError("Invalid owner_id")
            place_data = dict(place_data)
            place_data["owner"] = owner
            del place_data["owner_id"]

        # If amenities provided, validate and convert IDs to objects
        if "amenities" in place_data:
            new_amenities = []
            for amenity_id in place_data["amenities"]:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError("Invalid amenity_id")
                new_amenities.append(amenity)
        # Replace amenities list
            place.amenities = []
            for a in new_amenities:
                place.add_amenity(a)

            place_data = dict(place_data)
            del place_data["amenities"]

        # Update remaining fields via model validation
        place.update(place_data)
        return place
    
    # REVIEW METHODS
    def create_review(self, review_data):
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")

        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("Invalid user_id")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Invalid place_id")

        review = Review(
            text=review_data.get("text"),
            rating=review_data.get("rating"),
            place=place,
            user=user
        )

        # link review to place (no DB, so we keep relation in memory)
        place.add_review(review)

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


    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False

        # remove from place.reviews if present
        place = getattr(review, "place", None)
        if place and getattr(place, "reviews", None):
            place.reviews = [r for r in place.reviews if r.id != review_id]

        self.review_repo.delete(review_id)
        return True
