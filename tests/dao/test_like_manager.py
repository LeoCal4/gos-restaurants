from tests.models.test_restaurant import TestRestaurant
from .dao_test import DaoTest
from random import randint

class TestLikeManager(DaoTest):

    @classmethod
    def setUpClass(cls):
        super(TestLikeManager, cls).setUpClass()
        from restaurants.dao import like_manager
        cls.like_manager = like_manager

    def test_create_delete(self):
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        customer_id = randint(0, 999) 

        from restaurants.dao.restaurant_manager import RestaurantManager

        # Adding restaurant
        RestaurantManager.create_restaurant(restaurant=restaurant)

        self.like_manager.LikeManager.create_like(customer_id, restaurant.id)
        self.like_manager.LikeManager.delete_like(customer_id, restaurant.id)

        self.assertEqual(
            False,
            self.like_manager.LikeManager.like_exists(
                restaurant_id=restaurant.id,
                user_id=customer_id
            )
        )
