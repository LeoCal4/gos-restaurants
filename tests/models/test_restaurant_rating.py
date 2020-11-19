import unittest
from random import randint

from faker import Faker

from .model_test import ModelTest


class TestRestaurantRating(ModelTest):
    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super(TestRestaurantRating, cls).setUpClass()

        from restaurants.models import restaurant, restaurant_rating

        cls.restaurant_rating = restaurant_rating
        cls.restaurant = restaurant

    @staticmethod
    def generate_random_rating(restaurant=None, customer_id=None):
        from restaurants.models.restaurant_rating import RestaurantRating

        from .test_restaurant import TestRestaurant
        
        if restaurant is None:
            restaurant, _ = TestRestaurant.generate_random_restaurant()
        
        if customer_id is None:
            customer_id = randint(0, 999)
        
        value = randint(RestaurantRating.MIN_VALUE, RestaurantRating.MAX_VALUE)
        review = TestRestaurantRating.faker.text(max_nb_chars=RestaurantRating.REVIEW_MAX_LENGTH)
        customer_name = TestRestaurantRating.faker.first_name()

        restaurant_rating = RestaurantRating(
            customer_id=customer_id,
            restaurant_id=restaurant.id,
            customer_name=customer_name,
            value=value,
            review=review
        )

        return restaurant_rating, (customer_id, customer_name, restaurant.id, value, review)

    
    @staticmethod
    def assertRatingEquals(r1, r2):
        t = unittest.FunctionTestCase(TestRestaurantRating)
        t.assertEqual(r1.customer_id, r2.customer_id)
        t.assertEqual(r1.restaurant_id, r2.restaurant_id)
        t.assertEqual(r1.customer_name, r2.customer_name)
        t.assertEqual(r1.value, r2.value)
        t.assertEqual(r1.review, r2.review)

    def test_init(self):
        for _ in range(0, 10):
            restaurant_rating, (customer_id, customer_name, restaurant_id, value, review) = TestRestaurantRating.generate_random_rating()

            self.assertEqual(restaurant_rating.review, review)
            self.assertEqual(restaurant_rating.value, value)
            self.assertEqual(restaurant_rating.customer_id, customer_id)
            self.assertEqual(restaurant_rating.customer_name, customer_name)
            self.assertEqual(restaurant_rating.restaurant_id, restaurant_id)

    def test_value(self):
        from restaurants.models.restaurant_rating import RestaurantRating

        for _ in range(0, 10):
            restaurant_rating, _ = TestRestaurantRating.generate_random_rating()
            restaurant_rating.set_value(
                randint(RestaurantRating.MIN_VALUE, RestaurantRating.MAX_VALUE)
            )

    def test_bad_value(self):
        from restaurants.models.restaurant_rating import RestaurantRating

        for _ in range(0, 10):
            restaurant_rating, _ = TestRestaurantRating.generate_random_rating()
            with self.assertRaises(ValueError):
                restaurant_rating.set_value(RestaurantRating.MIN_VALUE - randint(1, 100))
                restaurant_rating.set_value(RestaurantRating.MAX_VALUE + randint(1, 100))

    def test_bad_review(self):
        from restaurants.models.restaurant_rating import RestaurantRating

        for _ in range(0, 10):
            restaurant_rating, _ = TestRestaurantRating.generate_random_rating()
            with self.assertRaises(ValueError):
                text = ''.join(['a' for _ in range(0, RestaurantRating.REVIEW_MAX_LENGTH + randint(1, 100))])
                restaurant_rating.set_review(text)

    def test_review(self):
        import textwrap

        from restaurants.models.restaurant_rating import RestaurantRating

        for _ in range(0, 10):
            restaurant_rating, _ = TestRestaurantRating.generate_random_rating()
            text = textwrap.shorten(TestRestaurantRating.faker.text(), RestaurantRating.REVIEW_MAX_LENGTH-1)
            restaurant_rating.set_review(text)
