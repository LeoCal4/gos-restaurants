import random
import unittest
from faker import Faker

from .model_test import ModelTest



class TestRestaurantAvailability(ModelTest):
    faker = Faker()
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']

    @classmethod
    def setUpClass(cls):
        super(TestRestaurantAvailability, cls).setUpClass()

        from restaurants.models import restaurant
        from restaurants.models import restaurant_availability
        cls.restaurant = restaurant
        cls.availability = restaurant_availability
        from .test_restaurant import TestRestaurant
        cls.test_restaurant = TestRestaurant


    @staticmethod
    def generate_correct_random_times():
        # generating times
        start_datetime = TestRestaurantAvailability.faker.date_time()
        end_datetime = start_datetime + TestRestaurantAvailability.faker.time_delta(1)

        return start_datetime.time(), end_datetime.time()

    @staticmethod
    def generate_random_availabilities(restaurants: list, max_ava=25):
        """
        It generates, for each restaurant a set of random availabilities
        :param max_ava: maximum availabilities
        :param restaurants: a list of restaturans
        :return: a list of a list of availabilities
        """
        from restaurants.models.restaurant_availability import RestaurantAvailability
        faker = Faker()
        rest_ava = []
        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        for rest in restaurants:
            avas = []
            for _ in range(0, random.randint(1, max_ava)):
                s, e = TestRestaurantAvailability.generate_correct_random_times()
                day = week_days[faker.random_int(min=0, max=6)]
                ava = RestaurantAvailability(
                    rest.id,
                    day,
                    s,
                    e
                )
                avas.append(ava)
            rest_ava.append(avas)

        return rest_ava

    @staticmethod
    def assertEqualAvailability(ra1, ra2):
        t = unittest.FunctionTestCase(TestRestaurantAvailability)
        t.assertEqual(ra1.start_time, ra2.start_time)
        t.assertEqual(ra1.end_time, ra2.end_time)
        t.assertEqual(ra1.restaurant.id, ra2.restaurant.id)

    def test_init(self):
        for _ in range(0, 10):
            restaurant, _ = self.test_restaurant.generate_random_restaurant()
            start_time, end_time = self.generate_correct_random_times()
            _avail = self.availability.RestaurantAvailability(
                restaurant.id,
                self.week_days[self.faker.random_int(min=0, max=6)],
                start_time,
                end_time
            )

            self.assertEqual(start_time, _avail.start_time)
            self.assertEqual(end_time, _avail.end_time)

    def test_set_times(self):
        for _ in range(0, 10):
            restaurant, _ = self.test_restaurant.generate_random_restaurant()
            start_time, end_time = self.generate_correct_random_times()
            _avail = self.availability.RestaurantAvailability(
                restaurant.id,
                self.week_days[self.faker.random_int(min=0, max=6)],
                start_time,
                end_time
            )
            _avail.set_times(start_time, end_time)

            self.assertEqual(start_time, _avail.start_time)
            self.assertEqual(end_time, _avail.end_time)
    
    def test_set_day(self):
        for _ in range(0, 10):
            restaurant, _ = self.test_restaurant.generate_random_restaurant()
            start_time, end_time = self.generate_correct_random_times()
            _avail = self.availability.RestaurantAvailability(
                restaurant.id,
                self.week_days[self.faker.random_int(min=0, max=6)],
                start_time,
                end_time
            )
            day = self.week_days[self.faker.random_int(min=0, max=6)]
            _avail.set_day(day)

            self.assertEqual(day, _avail.day)