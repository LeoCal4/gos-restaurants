import unittest


class ResourceTest(unittest.TestCase):
    """
    This class should be implemented by
    all classes that tests resources
    """
    client = None

    @classmethod
    def setUpClass(cls):
        from restaurants import create_app
        app = create_app()
        cls.client = app.test_client()
        from tests.models.test_restaurant import TestRestaurant
        cls.test_restaurant = TestRestaurant
        from restaurants.dao import restaurant_manager
        cls.restaurant_manager = restaurant_manager.RestaurantManager
        from tests.models.test_table import TestTable
        cls.test_table = TestTable
        from restaurants.dao import table_manager
        cls.table_manager = table_manager.TableManager
        from tests.models.test_restaurant_availability import TestRestaurantAvailability
        cls.test_restaurant_ava = TestRestaurantAvailability
        from restaurants.dao import restaurant_availability_manager
        cls.restaurant_ava_manager = restaurant_availability_manager.RestaurantAvailabilityManager