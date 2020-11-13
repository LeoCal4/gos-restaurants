import random
import unittest
from faker import Faker

from .model_test import ModelTest


class TestRestaurantRating(ModelTest):
    fake = Faker()

    @classmethod
    def setUpClass(cls):
        super(TestRestaurantRating, cls).setUpClass()

        from restaurants.models import restaurant_rating
        from restaurants.models import customer
        from restaurants.models import restaurant

        cls.restaurant_rating = restaurant_rating
        cls.customer = customer
        cls.restaurant = restaurant

    def test_init(self):
        for _ in range(0, 10):
            restaurant_rating, (customer, restaurant, value, review) = TestRestaurantRating.generate_random_rating()

            self.assertEqual(restaurant_rating.review, review)
            self.assertEqual(restaurant_rating.value, value)
            self.assertEqual(restaurant_rating.customer_id, customer.id)
            self.assertEqual(restaurant_rating.restaurant_id, restaurant.id)

    def test_value(self):
        from restaurants.models.restaurant_rating import RestaurantRating

        for _ in range(0, 10):
            restaurant_rating, _ = TestRestaurantRating.generate_random_rating()
            restaurant_rating.set_value(
                random.randint(RestaurantRating.MIN_VALUE, RestaurantRating.MAX_VALUE)
            )

    def test_bad_value(self):
        from restaurants.models.restaurant_rating import RestaurantRating

        for _ in range(0, 10):
            restaurant_rating, _ = TestRestaurantRating.generate_random_rating()
            with self.assertRaises(ValueError):
                restaurant_rating.set_value(RestaurantRating.MIN_VALUE - random.randint(1, 100))
                restaurant_rating.set_value(RestaurantRating.MAX_VALUE + random.randint(1, 100))

    def test_bad_review(self):
        from restaurants.models.restaurant_rating import RestaurantRating

        for _ in range(0, 10):
            restaurant_rating, _ = TestRestaurantRating.generate_random_rating()
            with self.assertRaises(ValueError):
                text = ''.join(['a' for _ in range(0, RestaurantRating.REVIEW_MAX_LENGTH + random.randint(1, 100))])
                restaurant_rating.set_review(text)

    def test_review(self):
        from restaurants.models.restaurant_rating import RestaurantRating
        import textwrap

        for _ in range(0, 10):
            restaurant_rating, _ = TestRestaurantRating.generate_random_rating()
            text = textwrap.shorten(TestRestaurantRating.fake.text(), RestaurantRating.REVIEW_MAX_LENGTH-1)
            restaurant_rating.set_review(text)

    @staticmethod
    def generate_random_rating(restaurant=None, customer=None):
        from .test_customer import TestCustomer
        from .test_restaurant import TestRestaurant
        from restaurants.models.restaurant_rating import RestaurantRating

        if restaurant is None and customer is None:
            customer, _ = TestCustomer.generate_random_customer()
            restaurant, _ = TestRestaurant.generate_random_restaurant()

        value = random.randint(RestaurantRating.MIN_VALUE, RestaurantRating.MAX_VALUE)
        review = TestRestaurantRating.fake.text(max_nb_chars=RestaurantRating.REVIEW_MAX_LENGTH)

        restaurant_rating = RestaurantRating(
            customer_id=customer.id,
            restaurant_id=restaurant.id,
            value=value,
            review=review
        )

        return restaurant_rating, (customer, restaurant, value, review)

    @staticmethod
    def assertRatingEquals(r1, r2):
        t = unittest.FunctionTestCase(TestRestaurantRating)
        t.assertEqual(r1.customer_id, r2.customer_id)
        t.assertEqual(r1.restaurant_id, r2.restaurant_id)
        t.assertEqual(r1.value, r2.value)
        t.assertEqual(r1.review, r2.review)
