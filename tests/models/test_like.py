from faker import Faker

from .model_test import ModelTest
from .test_customer import TestCustomer
from .test_restaurant import TestRestaurant


class TestLike(ModelTest):
    faker = Faker('it_IT')

    @classmethod
    def generate_random_likes(cls):
        # Generate random restaurants
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        customer, _ = TestCustomer.generate_random_customer()

        from restaurants.models.like import Like
        like = Like(
            restaurant=restaurant,
            liker=customer
        )

        return like, (restaurant, customer)

    def setUp(self):
        super(TestLike, self).setUp()

        from restaurants.models import like
        from restaurants.models import restaurant

        self.like = like.Like
        self.restaurant = restaurant.Restaurant

    def test_init(self):
        like, (restaurant, user) = self.generate_random_likes()

        self.assertEqual(like.restaurant.id, restaurant.id)
        self.assertEqual(like.restaurant_id, restaurant.id)
        self.assertEqual(like.liker, user)
        self.assertEqual(like.liker_id, user.id)
