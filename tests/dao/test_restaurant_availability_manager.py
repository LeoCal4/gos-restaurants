from faker import Faker
from .dao_test import DaoTest


class TestRestaurantAvailabilityManager(DaoTest):
    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super(TestRestaurantAvailabilityManager, cls).setUpClass()

        from tests.models.test_restaurant import TestRestaurant
        cls.test_restaurant = TestRestaurant
        from tests.models.test_restaurant_availability import TestRestaurantAvailability
        cls.test_restaurant_availability = TestRestaurantAvailability
        from restaurants.dao import restaurant_availability_manager
        from restaurants.dao import restaurant_manager
        from restaurants.models import restaurant_availability
        cls.ram = restaurant_availability_manager.RestaurantAvailabilityManager
        cls.ava = restaurant_availability
        cls.re_ma = restaurant_manager

    def test_crud(self):
        rests = []
        for _ in range(0, 10):
            restaurant, _ = self.test_restaurant.generate_random_restaurant()
            self.re_ma.RestaurantManager.create_restaurant(restaurant)
            rests.append(restaurant)

        rests_ava = self.test_restaurant_availability.generate_random_availabilities(
            rests
        )

        # test create
        for avas in rests_ava:
            for ava in avas:
                self.ram.create_availability(ava)

        # test update
        for avas in rests_ava:
            for ava in avas:
                s, e = self.test_restaurant_availability.generate_correct_random_times()
                ava.set_times(s, e)
                self.ram.update_availability(ava)

        # test delete
        for avas in rests_ava:
            for ava in avas:
                self.ram.delete_availability(ava)
