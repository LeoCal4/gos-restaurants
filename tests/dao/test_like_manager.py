from tests.models.test_customer import TestCustomer
from tests.models.test_restaurant import TestRestaurant
from .dao_test import DaoTest


class TestLikeManager(DaoTest):

    @classmethod
    def setUpClass(cls):
        super(TestLikeManager, cls).setUpClass()
        from restaurants.dao import like_manager
        cls.like_manager = like_manager

    def test_create_delete(self):
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        customer, _ = TestCustomer.generate_random_customer()

        from restaurants.dao.customer_manager import CustomerManager
        from restaurants.dao.restaurant_manager import RestaurantManager

        # Adding restaurant
        RestaurantManager.create_restaurant(restaurant=restaurant)
        # Adding user
        CustomerManager.create_customer(customer=customer)

        self.like_manager.LikeManager.create_like(customer.id, restaurant.id)
        self.like_manager.LikeManager.delete_like(customer.id, restaurant.id)

        self.assertEqual(
            False,
            self.like_manager.LikeManager.like_exists(
                restaurant_id=restaurant.id,
                user_id=customer.id
            )
        )
