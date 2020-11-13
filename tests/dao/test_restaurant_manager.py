from faker import Faker

from .dao_test import DaoTest


class TestRestaurantManager(DaoTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestRestaurantManager, cls).setUpClass()
        
        from tests.models.test_restaurant import TestRestaurant
        cls.test_restaurant = TestRestaurant
        from tests.models.test_operator import TestOperator
        cls.test_operator = TestOperator
        from restaurants.dao import restaurant_manager
        cls.restaurant_manager = restaurant_manager.RestaurantManager
        from restaurants.dao import customer_manager
        cls.customer_manager = customer_manager.CustomerManager
    
    def test_create_restaurant(self):
        restaurant1, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant=restaurant1)
        restaurant2 = self.restaurant_manager.retrieve_by_id(id_=restaurant1.id)
        self.test_restaurant.assertEqualRestaurants(restaurant1, restaurant2)
    
    def test_delete_restaurant(self):
        base_restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant=base_restaurant)
        self.restaurant_manager.delete_restaurant(base_restaurant)
        self.assertIsNone(self.restaurant_manager.retrieve_by_id(base_restaurant.id))

    def test_delete_restaurant_by_id(self):
        base_restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant=base_restaurant)
        self.restaurant_manager.delete_restaurant_by_id(base_restaurant.id)
        self.assertIsNone(self.restaurant_manager.retrieve_by_id(base_restaurant.id))

    def test_update_restaurant(self):
        base_restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant=base_restaurant)
        base_restaurant.set_address(TestRestaurantManager.faker.street_address())
        base_restaurant.set_city(TestRestaurantManager.faker.city())
        updated_restaurant = self.restaurant_manager.retrieve_by_id(id_=base_restaurant.id)
        self.test_restaurant.assertEqualRestaurants(base_restaurant, updated_restaurant)

    def test_retrieve_by_operator_id(self):
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        operator, _ = self.test_operator.generate_random_operator()
        restaurant.owner = operator
        self.restaurant_manager.create_restaurant(restaurant=restaurant)
        self.customer_manager.create_customer(customer=operator)
        retrieved_restaurant = self.restaurant_manager.retrieve_by_operator_id(operator_id=operator.id)
        self.test_restaurant.assertEqualRestaurants(restaurant, retrieved_restaurant)
    
    def test_retrieve_by_menu_type(self):
        menu_type = 'Italian'
        for _ in range(0, 10):
            restaurant, _ = self.test_restaurant.generate_random_restaurant()
            restaurant.set_menu_type(menu_type)
            self.restaurant_manager.create_restaurant(restaurant)
        retrieved_restaurants = self.restaurant_manager.retrieve_by_menu_type(menu_type).all()
        for res in retrieved_restaurants:
            self.assertEqual(menu_type, res.menu_type)

    def test_retrieve_by_restaurant_name(self):
        name = 'Pizza da Musca'
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        restaurant.set_name(name)
        self.restaurant_manager.create_restaurant(restaurant)
        retrieved_restaurants = self.restaurant_manager.retrieve_by_restaurant_name(name).all()
        for res in retrieved_restaurants:
            self.assertEqual(name, res.name)

    def test_retrieve_by_restaurant_city(self):
        city = 'Muscacity'
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        restaurant.set_city(city)
        self.restaurant_manager.create_restaurant(restaurant)
        retrieved_restaurants = self.restaurant_manager.retrieve_by_restaurant_city(city).all()
        for res in retrieved_restaurants:
            self.assertEqual(city, res.city)
