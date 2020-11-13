from .dao_test import DaoTest
from tests.models.test_restaurant_rating import TestRestaurantRating
from tests.models.test_customer import TestCustomer
from tests.models.test_restaurant import TestRestaurant
from faker import Faker



class RestaurantRatingManagerTest(DaoTest):
    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super(RestaurantRatingManagerTest, cls).setUpClass()

        from restaurants.dao import restaurant_rating_manager
        cls.rating_manager = restaurant_rating_manager.RestaurantRatingManager
        from restaurants.dao import restaurant_manager
        cls.restaurant_manager = restaurant_manager.RestaurantManager
        from restaurants.dao import customer_manager
        cls.customer_manager = customer_manager.CustomerManager

    def test_create_delete(self):
        """
        @TODO it will be implemented when restaurant dao will be done
        :return:
        """

        for _ in range(0, 10):
            customer, _ = TestCustomer.generate_random_customer()
            self.customer_manager.create_customer(customer)
            restaurant, _= TestRestaurant.generate_random_restaurant()
            self.restaurant_manager.create_restaurant(restaurant)
            rating,_ = TestRestaurantRating.generate_random_rating(restaurant=restaurant, customer=customer)
            self.rating_manager.create_rating(rating)
            self.assertTrue(self.rating_manager.check_existence(restaurant.id, customer.id))
            rating.set_value(self.faker.random_int(min=0,max=10))
            self.rating_manager.update_rating(rating)
            rating1 = self.rating_manager.retrieve_by_restaurant_customer(restaurant.id, customer.id)
            TestRestaurantRating.assertRatingEquals(rating1, rating)
            self.rating_manager.delete_rating(rating)
        
    def test_calculate_average_rate(self):
        restaurant, _= TestRestaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        values = []
        for _ in range(0, 10):
            customer, _ = TestCustomer.generate_random_customer()
            self.customer_manager.create_customer(customer)
            rating,_ = TestRestaurantRating.generate_random_rating(restaurant=restaurant, customer=customer)
            values.append(rating.value)
            self.rating_manager.create_rating(rating)
        avg = sum(values) / len(values)
        retrieved_avg = self.rating_manager.calculate_average_rate(restaurant)
        self.assertEqual(avg, retrieved_avg)
        restaurant_no_ratings, _= TestRestaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant_no_ratings)
        retrieved_avg = self.rating_manager.calculate_average_rate(restaurant_no_ratings)
        self.assertIsNone(retrieved_avg)
            