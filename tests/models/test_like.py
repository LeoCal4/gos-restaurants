from random import randint

from faker import Faker

from .model_test import ModelTest
from .test_restaurant import TestRestaurant


class TestLike(ModelTest):
    faker = Faker('it_IT')

    @classmethod
    def generate_random_likes(cls):
        # Generate random restaurants
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        customer_id = randint(0, 999)

        from restaurants.models.like import Like
        like = Like(
            restaurant=restaurant,
            liker_id=customer_id
        )

        return like, (restaurant, customer_id)

    def setUp(self):
        super(TestLike, self).setUp()

        from restaurants.models import like, restaurant

        self.like = like.Like
        self.restaurant = restaurant.Restaurant

    def test_init(self):
        like, (restaurant, user_id) = self.generate_random_likes()

        self.assertEqual(like.restaurant.id, restaurant.id)
        self.assertEqual(like.liker_id, user_id)
