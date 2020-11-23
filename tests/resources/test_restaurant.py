from datetime import time
from random import randint, choice

from faker import Faker

from .resource_test import ResourceTest


class RestaurantResTest(ResourceTest):
    faker = Faker()


    @classmethod
    def setUpClass(cls):
        super(RestaurantResTest, cls).setUpClass()
        from restaurants.dao.restaurant_manager import RestaurantManager
        cls.restaurant_manager = RestaurantManager
        from tests.models.test_restaurant import TestRestaurant
        cls.test_restaurant = TestRestaurant 
        from tests.models.test_restaurant_availability import \
            TestRestaurantAvailability
        cls.test_availability = TestRestaurantAvailability
        from tests.models.test_restaurant_rating import TestRestaurantRating
        cls.test_restaurant_rating = TestRestaurantRating

    def test_restaurant_sheet_400(self):
    #Test unsuccessful response, the restaurant doens't exists
        response = self.client.get('/restaurant/' + str(0))
        assert response.status_code == 400

    def test_restaurant_sheet_200(self):
    #Test successful response
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        response = self.client.get('/restaurant/' + str(restaurant.id))
        assert response.status_code == 200

    def test_get_by_op_id_200(self):
        _, op_id, _ = self.add_restaurant()
        response = self.client.get('/restaurant/by_operator_id/' + str(op_id))
        assert response.status_code == 200

    def test_get_by_op_id_400(self):
        #Test unsuccessful response, the restaurant doesn't exists
        response = self.client.get('/restaurant/by_operator_id/' + str(0))
        assert response.status_code == 400

    def test_get_all_restaurant_200(self):
    #Test successful response
        restaurants = []
        for _ in range(randint(2, 10)):
            restaurant, _ = self.test_restaurant.generate_random_restaurant()
            self.restaurant_manager.create_restaurant(restaurant)
            restaurants.append(restaurant)
        response = self.client.get('/restaurant/all')
        assert response.status_code == 200
    
    def test_search_by_200(self):
        #Test successful response
        search_field = choice(['Menu Type', 'City', 'Name'])
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        restaurant.menu_type = search_field
        name = restaurant.name
        self.restaurant_manager.create_restaurant(restaurant)
        response = self.client.get('/restaurant/search_by/%s/%s' % (name, search_field))
        assert response.status_code == 200

    def test_like_toggle_400(self):
    #Test unsuccessful response, bad input data
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        data = {}
        response = self.client.put('/restaurant/like/' + str(restaurant.id), json=data)
        assert response.status_code == 400

    def test_like_toggle_200(self):
    #Test successful response
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        data = {'user_id': 1 }
        response = self.client.put('/restaurant/like/' + str(restaurant.id), json=data)
        assert response.status_code == 200

    def test_like_toggle_500(self):
    #Test DB error response
        data = {'user_id': 2 }
        response = self.client.put('/restaurant/like/' + str(0), json=data)
        assert response.status_code == 500

    def test_post_add_400(self):
    #Test wrong input data
        data = {}
        response = self.client.post('/restaurant', json=data)
        assert response.status_code == 400

    def test_post_add_200(self):
    #Test successful adding new restaurant
        restaurant, _, _ = self.add_restaurant()
        data = {'name': restaurant.name,
                'address': restaurant.address,
                'city':  restaurant.city,
                'phone': restaurant.phone,
                'menu_type': restaurant.menu_type,
                'op_id': restaurant.owner_id}
        response = self.client.post('/restaurant', json=data)
        assert response.status_code == 200

    def test_add_tables_200(self):
        restaurant, _, _ = self.add_restaurant()
        data = {'number': self.faker.random_int(min=1, max=10),
                'max_capacity': self.faker.random_int(min=1, max=10)}
        response = self.client.post('/restaurant/tables/'+ str(restaurant.id), json=data)
        assert response.status_code == 200

    def test_add_tables_400(self):
        response = self.client.post('/restaurant/tables/' + str(0), json={})
        assert response.status_code == 400

    def test_add_times_200(self):
        restaurant, _, _ = self.add_restaurant()
        start_time = time(hour=self.faker.random_int(min=0, max=12), minute=self.faker.random_int(min=0, max=59))
        end_time = time(hour=self.faker.random_int(min=13, max=23), minute=self.faker.random_int(min=0, max=59))
        data = {'day': 'Monday',
                'start_time': start_time.strftime('%H:%M:%S'),
                'end_time': end_time.strftime('%H:%M:%S')}
        response = self.client.post('/restaurant/time/' + str(restaurant.id), json=data)
        assert response.status_code == 200

    def test_add_times_400(self):
        response = self.client.post('/restaurant/time/' + str(0), json={})
        assert response.status_code == 400
        restaurant, _, _ = self.add_restaurant()
        response = self.client.post('/restaurant/time/' + str(restaurant.id), json={})
        assert response.status_code == 400   

    def test_add_measure_200(self):
        list_measure = ["Hand sanitizer", "Plexiglass", "Spaced tables",
                    "Sanitized rooms", "Temperature scanners"]        
        restaurant, _, _ = self.add_restaurant()
        test_measure = list_measure[self.faker.random_int(min=0, max=4)]
        data = {'measure' : test_measure}
        response = self.client.put('/restaurant/measure/' + str(restaurant.id), json=data)
        assert response.status_code == 200

    def test_add_measure_400(self):
        response = self.client.put('/restaurant/measure/' + str(0), json={})
        assert response.status_code == 400
        restaurant, _, _ = self.add_restaurant()
        response = self.client.put('/restaurant/measure/' + str(restaurant.id), json={})
        assert response.status_code == 400

    def test_add_avg_stay_200(self):      
        restaurant, _, _ = self.add_restaurant()
        hours = self.faker.random_int(min=0, max=23)
        minutes = self.faker.random_int(min=1, max=59)
        data = {'hours' : hours,
                'minutes': minutes}
        response = self.client.put('/restaurant/avg_stay/' + str(restaurant.id), json=data)
        assert response.status_code == 200

    def test_add_avg_stay_400(self):
        response = self.client.put('/restaurant/avg_stay/' + str(0), json={})
        assert response.status_code == 400
        restaurant, _, _ = self.add_restaurant()
        response = self.client.put('/restaurant/avg_stay/' + str(restaurant.id), json={})
        assert response.status_code == 400

    def test_post_edit_restaurant_400(self):
        response = self.client.put('restaurant/' + str(0), json={})
        assert response.status_code == 400
        restaurant, _, _ = self.add_restaurant()
        response = self.client.put('restaurant/' + str(restaurant.id), json={})
        assert response.status_code == 400

    def test_post_edit_restaurant_200(self):
        restaurant, _, data = self.add_restaurant()
        response = self.client.put('restaurant/' + str(restaurant.id), json=data)
        assert response.status_code == 200

    def test_delete_restaurant_400(self):
        response = self.client.delete('restaurant/' + str(0))
        assert response.status_code == 400

    def test_delete_restaurant_200(self):
        restaurant, _, _ = self.add_restaurant()
        response = self.client.delete('restaurant/' + str(restaurant.id))
        restaurant = self.restaurant_manager.retrieve_by_id(restaurant.id)
        self.assertIsNone(restaurant)
        assert response.status_code == 200
    
    def test_add_review_200(self):
        restaurant, _, _ = self.add_restaurant()
        restaurant_id = restaurant.id
        review, _ = self.test_restaurant_rating.generate_random_rating(restaurant=restaurant)
        review = review.serialize()
        response = self.client.post('restaurant/review', json=review)
        restaurant = self.restaurant_manager.retrieve_by_id(restaurant_id)
        review, _ = self.test_restaurant_rating.generate_random_rating(restaurant=restaurant, customer_id=review['customer_id'])
        review = review.serialize()
        response = self.client.post('restaurant/review', json=review)
        assert response.status_code == 200

    def test_add_review_201(self):
        restaurant, _, _ = self.add_restaurant()
        review, _ = self.test_restaurant_rating.generate_random_rating(restaurant=restaurant)
        review = review.serialize()
        response = self.client.post('restaurant/review', json=review)
        assert response.status_code == 201

    def test_add_review_400(self):
        restaurant, _, _ = self.add_restaurant()
        review, _ = self.test_restaurant_rating.generate_random_rating(restaurant=restaurant)
        review = review.serialize()
        del review['value']
        response = self.client.post('restaurant/review', json=review)
        assert response.status_code == 400

    def test_get_rating_bounds_200(self):
        response = self.client.get('restaurant/rating_bounds')
        assert response.status_code == 200
        
    #Tests on Helper Methods

    def test_toggle_like(self):
        pass

    def test_convert_avg_stay_fromat_0(self):
        from restaurants.resources.restaurants import convert_avg_stay_format
        avg_stay = None
        self.assertEqual('0', convert_avg_stay_format(avg_stay))

    def test_convert_avg_stay_fromat(self):
        from restaurants.resources.restaurants import convert_avg_stay_format
        avg_stay = self.faker.random_int(min=0, max=1440)
        h_avg_stay = avg_stay // 60
        m_avg_stay = avg_stay - (h_avg_stay * 60)
        computed_avg_stay = "%dH:%dM" % (h_avg_stay, m_avg_stay)
        self.assertEqual(computed_avg_stay, convert_avg_stay_format(avg_stay))

    def test_validate_ava_error(self):
        from restaurants.resources.restaurants import validate_ava
        restaurant, _, _ = self.add_restaurant()
        start_time = time(hour=self.faker.random_int(min=12, max=23), minute=self.faker.random_int(min=0, max=59))
        end_time = time(hour=self.faker.random_int(min=0, max=11), minute=self.faker.random_int(min=0, max=59))
        with self.assertRaises(ValueError):
            validate_ava(restaurant, 'Monady', start_time, end_time)        

    def test_validate_ava_true(self):
        from restaurants.resources.restaurants import validate_ava
        restaurant, _, _ = self.add_restaurant()
        start_time = time(hour=self.faker.random_int(min=0, max=12), minute=self.faker.random_int(min=0, max=59))
        end_time = time(hour=self.faker.random_int(min=13, max=23), minute=self.faker.random_int(min=0, max=59))
        self.assertTrue(validate_ava(restaurant, 'Monday', start_time, end_time))
        self.assertTrue(validate_ava(restaurant, 'Monday', start_time, end_time))
        self.assertTrue(validate_ava(restaurant, 'Sunday', start_time, end_time))

    #Helper method
    def add_restaurant(self):
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        id_operator = self.faker.random_int(min=0, max=50000)
        restaurant.owner_id = id_operator
        self.restaurant_manager.create_restaurant(restaurant)       
        data = {'name': restaurant.name,
                'address': restaurant.address,
                'city':  restaurant.city,
                'phone': restaurant.phone,
                'menu_type': restaurant.menu_type}
        return restaurant, id_operator, data
