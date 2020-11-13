import unittest

from .view_test import ViewTest


class TestReviewViews(ViewTest):

    @classmethod
    def setUpClass(cls):
        super(TestReviewViews, cls).setUpClass()
        from restaurants.dao.restaurant_manager import RestaurantManager
        cls.restaurant_manager = RestaurantManager
        from tests.models.test_restaurant import TestRestaurant
        cls.test_restaurant = TestRestaurant 
        from tests.models.test_restaurant_availability import TestRestaurantAvailability
        cls.test_availability = TestRestaurantAvailability
        from tests.models.test_restaurant_rating import TestRestaurantRating
        cls.test_restaurant_rating = TestRestaurantRating
        from restaurants.dao.restaurant_rating_manager import RestaurantRatingManager
        cls.rating_manager = RestaurantRatingManager

    def test_write_review_get(self):
        operator = self.login_test_operator()
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        restaurant.owner_id = operator.id
        self.restaurant_manager.create_restaurant(restaurant)
        rv = self.client.get('/restaurants/' + str(restaurant.id) + '/review', follow_redirects=True)
        assert rv.status_code == 200
    
    def test_write_review_thank(self):
        customer = self.login_test_customer()
        operator, _ = self.test_operator.generate_random_operator()
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.operator_manager.create_operator(operator)
        restaurant.owner_id = operator.id
        self.restaurant_manager.create_restaurant(restaurant)
        rating, _ = self.test_restaurant_rating.generate_random_rating(restaurant=restaurant, customer=customer)
        self.rating_manager.create_rating(rating)
        rv = self.client.get('/restaurants/' + str(restaurant.id) + '/review', follow_redirects=True)
        assert rv.status_code == 200
    
    def test_write_review_post(self):
        customer = self.login_test_customer()
        operator, _ = self.test_operator.generate_random_operator()
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.operator_manager.create_operator(operator)
        restaurant.owner_id = operator.id
        self.restaurant_manager.create_restaurant(restaurant)
        data = {'value': 5, 'review': 'ciao'}
        rv = self.client.post('/restaurants/' + str(restaurant.id) + '/review', data=data, follow_redirects=True)
        assert rv.status_code == 200
