from restaurants.dao.manager import Manager
from restaurants.models.restaurant_rating import RestaurantRating
from restaurants.models.restaurant import Restaurant
from sqlalchemy import func


class RestaurantRatingManager(Manager):
    """
    List of ratings are implemented
    in the Restaurant DAO and User DAO
    """

    @staticmethod
    def create_rating(rating: RestaurantRating):
        Manager.create(rating=rating)

    @staticmethod
    def delete_rating(rating: RestaurantRating):
        Manager.delete(rating=rating)

    @staticmethod
    def update_rating(rating: RestaurantRating):
        Manager.update(rating=rating)

    @staticmethod
    def retrieve_limited_ratings(restaurant: Restaurant, max_ratings: int):
        ratings = RestaurantRating.query.filter_by(restaurant=restaurant)
        return ratings.limit(max_ratings).all()

    @staticmethod
    def retrieve_by_restaurant_customer(restaurant_id, user_id):
        return RestaurantRating.query.filter_by(restaurant_id=restaurant_id, customer_id=user_id).first()

    @staticmethod
    def calculate_average_rate(restaurant: Restaurant):
        base_query = Manager.db_session.query(
            func.avg(RestaurantRating.value)
        ).filter_by(restaurant=restaurant)
        scalar = base_query.scalar()

        if scalar is None:
            return None
        return float(scalar)

    @staticmethod
    def check_existence(restaurant_id, user_id):
        base_query = RestaurantRating.query.filter_by(restaurant_id=restaurant_id, customer_id=user_id)

        return base_query.count() != 0
