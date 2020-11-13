from .manager import Manager
from restaurants.models.restaurant_availability import RestaurantAvailability


class RestaurantAvailabilityManager(Manager):
    """
    This manager does not implement the retrieve method
    because if you want to access the availabilities
    you must use the Restaurant.availabilities object.
    """

    @staticmethod
    def create_availability(ava: RestaurantAvailability):
        Manager.create(availability=ava)

    @staticmethod
    def delete_availability(ava: RestaurantAvailability):
        Manager.delete(availability=ava)

    @staticmethod
    def update_availability(ava: RestaurantAvailability):
        Manager.update(availability=ava)
