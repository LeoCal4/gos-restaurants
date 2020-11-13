import unittest

from .view_test import ViewTest


class TestRestaurantViews(ViewTest):

    @classmethod
    def setUpClass(cls):
        super(TestRestaurantViews, cls).setUpClass()
        from gooutsafe.dao.restaurant_manager import RestaurantManager
        cls.restaurant_manager = RestaurantManager
        from tests.models.test_restaurant import TestRestaurant
        cls.test_restaurant = TestRestaurant 
        from tests.models.test_restaurant_availability import TestRestaurantAvailability
        cls.test_availability = TestRestaurantAvailability

    def test_my_restaurant(self):
        #self.login_test_customer()
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        rv = self.client.get('/my_restaurant', follow_redirects=True)
        assert rv.status_code == 200

    def test_restaurants_sheet(self):
        #self.login_test_customer()
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        rv = self.client.get('/restaurants/' + str(restaurant.id))
        assert rv.status_code == 200

    def test_like_toggle(self):
        #self.login_test_customer()
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        rv = self.client.get('/restaurants/like/' + str(restaurant.id), follow_redirects=True)
        assert rv.status_code == 200

    def test_add_get(self):
        #owner = self.login_test_customer()
        onwer_id = 0
        rv = self.client.get('/restaurants/add/' + str(owner_id), follow_redirects=True)
        assert rv.status_code == 200
    
    def test_add_post(self):
        # owner = self.login_test_operator()
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        data = {'name': restaurant.name, 'address': restaurant.address, 'city': restaurant.city,
                'phone': str(restaurant.phone)}
        rv = self.client.post('/restaurants/add/' + str(owner.id), data=data, follow_redirects=True)
        assert rv.status_code == 200

    def test_details_get(self):
        # customer = self.login_test_customer()
        customer_id = 0
        rv = self.client.get('/restaurants/details/' + str(customer_id), follow_redirects=True)
        assert rv.status_code == 200

    def test_details_post(self):
        # operator = self.login_test_operator()
        operator_id = 0
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        restaurant.owner_id = operator_id
        self.restaurant_manager.create_restaurant(restaurant)
        rv = self.client.post('/restaurants/details/' + str(operator_id), follow_redirects=True)
        assert rv.status_code == 200

    def test_save_details_get(self):
        #customer = self.login_test_customer()
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        rv = self.client.get('/restaurants/save/' + str(customer.id) + '/' + str(restaurant.id), follow_redirects=True)
        assert rv.status_code == 200

    def test_save_details_post(self):
        owner = self.login_test_operator()
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        restaurant.owner_id = owner.id
        self.restaurant_manager.create_restaurant(restaurant)
        data = {'number': 10, 'max_capacity': 5}
        rv = self.client.post('/restaurants/save/' + str(owner.id) + '/' + str(restaurant.id), data=data, follow_redirects=True)
        assert rv.status_code == 200

    def test_save_time_get(self):
        customer = #self.login_test_customer()
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        rv = self.client.get('/restaurants/savetime/' + str(customer.id) + '/' +  str(restaurant.id), follow_redirects=True)
        assert rv.status_code == 200

    """def test_save_time_post(self):
        customer = #self.login_test_customer()
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        start_time, end_time = self.test_availability.generate_correct_random_times()
        data = {'day': 'Monday', 'start_time': start_time, 'end_time': end_time}
        rv = self.client.post('/restaurants/savetime/' + str(customer.id) + '/' + str(restaurant.id), data=data, follow_redirects=True)
        assert rv.status_code == 200"""

    def test_save_measure_get(self):
        customer = #self.login_test_customer()
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        rv = self.client.get('/restaurants/savemeasure/' + str(customer.id) + '/' +  str(restaurant.id), follow_redirects=True)
        assert rv.status_code == 200

    def test_save_measure_post(self):
        owner = self.login_test_operator()
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        restaurant.owner_id = owner.id
        self.restaurant_manager.create_restaurant(restaurant)
        data = {'measure': 10}
        rv = self.client.post('/restaurants/savemeasure/' + str(owner.id) + '/' + str(restaurant.id), data=data, follow_redirects=True)
        assert rv.status_code == 200

    def test_edit_restaurant_get(self):
        owner = #self.login_test_customer()
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        rv = self.client.get('/edit_restaurant/' + str(owner.id) + '/' + str(restaurant.id), follow_redirects=True)
        assert rv.status_code == 200
    
    def test_edit_restaurant_post(self):
        customer = self.login_test_operator()
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        data = {'name': restaurant.name, 'address': restaurant.address, 'city': restaurant.city,
                'phone': restaurant.phone, 'menu_type': restaurant.menu_type}
        rv = self.client.post('/edit_restaurant/' + str(customer.id) + '/' + str(restaurant.id), data=data, follow_redirects=True)
        assert rv.status_code == 200

    def test_save_avg_stay_get(self):
        owner = self.login_test_operator()
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        rv = self.client.get('/restaurants/avgstay/' + str(owner.id) + '/' + str(restaurant.id), follow_redirects=True)
        assert rv.status_code == 200
    
    def test_save_avg_stay_post(self):
        operator = self.login_test_operator()
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        restaurant.owner_id = operator.id
        self.restaurant_manager.create_restaurant(restaurant)
        data = {'hours': 1, 'minutes': 10}
        rv = self.client.post('/restaurants/avgstay/' + str(operator.id) + '/' + str(restaurant.id), data=data, follow_redirects=True)
        assert rv.status_code == 200


