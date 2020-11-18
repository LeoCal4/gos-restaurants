from .resource_test import ResourceTest
from faker import Faker
from datetime import time



class RestaurantResTest(ResourceTest):
    faker = Faker()


    @classmethod
    def setUpClass(cls):
        super(RestaurantResTest, cls).setUpClass()
        from restaurants.dao.restaurant_manager import RestaurantManager
        cls.restaurant_manager = RestaurantManager
        from tests.models.test_restaurant import TestRestaurant
        cls.test_restaurant = TestRestaurant 
        from tests.models.test_restaurant_availability import TestRestaurantAvailability
        cls.test_availability = TestRestaurantAvailability

    def test_restaurant_sheet_400(self):
    #Test unsuccessful response, the restaurant doens't exists
        response = self.client.get('/restaurants/' + str(0))
        assert response.status_code == 400

    def test_restaurant_sheet_200(self):
    #Test successful response
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        response = self.client.get('/restaurants/' + str(restaurant.id))
        json_response = response.json
        assert response.status_code == 200       

    def test_like_toggle_400(self):
    #Test unsuccessful response, bad input data
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        data = {}
        response = self.client.post('/restaurants/like/' + str(restaurant.id), json=data)
        json_response = response.json
        assert response.status_code == 400

    def test_like_toggle_200(self):
    #Test successful response
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        data = {'user_id': '1' }
        response = self.client.post('/restaurants/like/' + str(restaurant.id), json=data)
        json_response = response.json
        assert response.status_code == 200

    def test_like_toggle_500(self):
    #Test DB error response
        data = {'user_id': '2' }
        response = self.client.post('/restaurants/like/' + str(0), json=data)
        json_response = response.json
        assert response.status_code == 500

    def test_post_add_400(self):
    #Test wrong input data
        data = {}
        id_operator = self.faker.random_int(min=1)
        response = self.client.post('/restaurants/add/' + str(id_operator), json=data)
        json_response = response.json
        assert response.status_code == 400

    def test_post_add_200(self):
    #Test successful adding new restaurant
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)       
        data = {'name': restaurant.name,
                'address': restaurant.address,
                'city':  restaurant.city,
                'phone': restaurant.phone,
                'menu_type': restaurant.menu_type}
        id_operator = self.faker.random_int(min=0, max=50000)
        response = self.client.post('/restaurants/add/' + str(id_operator), json=data)
        json_response = response.json
        assert response.status_code == 200

    def test_details_400(self):
    #Test the restaurant doesn't exists
        response = self.client.get('/restaurants/details/' + str(0))
        assert response.status_code == 400

    def test_details_200(self):
    #Test successful retrive
        restaurant, id_operator, data = self.add_restaurant()
        self.client.post('/restaurants/add/' + str(id_operator), json=data)
        response = self.client.get('/restaurants/details/' + str(id_operator))
        assert response.status_code == 200

    def test_add_tables_400(self):
        response = self.client.post('/restaurants/add_tables/'+ str(0) + '/' + str(0), json={})
        assert response.status_code == 400

    def test_add_tables_200(self):
        restaurant, id_operator, _ = self.add_restaurant()
        data = {'number': self.faker.random_int(min=1, max=10),
                'max_capacity': self.faker.random_int(min=1, max=10)}
        response = self.client.post('/restaurants/add_tables/'+ str(id_operator) + '/' + str(restaurant.id), json=data)
        assert response.status_code == 200
        

    def test_add_times_400(self):
        response = self.client.post('/restaurants/add_time/'+ str(0) + '/' + str(0), json={})
        assert response.status_code == 400
        restaurant, id_operator, _ = self.add_restaurant()
        response = self.client.post('/restaurants/add_time/'+ str(id_operator) + '/' + str(restaurant.id), json={})
        assert response.status_code == 400   
            
    def test_add_times_200(self):
        restaurant, id_operator, _ = self.add_restaurant()
        start_time = time(hour=self.faker.random_int(min=0, max=12), minute=self.faker.random_int(min=0, max=59))
        end_time = time(hour=self.faker.random_int(min=13, max=23), minute=self.faker.random_int(min=0, max=59))
        data = {'day': 'Monday',
                'start_time': start_time.strftime('%H:%M'),
                'end_time': end_time.strftime('%H:%M')}
        response = self.client.post('/restaurants/add_time/'+ str(id_operator) + '/' + str(restaurant.id), json=data)
        assert response.status_code == 200
    
    def test_add_measure_400(self):
        response = self.client.post('/restaurants/add_measure/' + str(0) + '/' + str(0), json={})
        assert response.status_code == 400
        restaurant, id_operator, _ = self.add_restaurant()
        response = self.client.post('/restaurants/add_measure/'+ str(id_operator) + '/' + str(restaurant.id), json={})
        assert response.status_code == 400
        json_response = response.json
    
    def test_add_measure_200(self):
        list_measure = ["Hand sanitizer", "Plexiglass", "Spaced tables",
                    "Sanitized rooms", "Temperature scanners"]        
        restaurant, id_operator, _ = self.add_restaurant()
        test_measure = list_measure[self.faker.random_int(min=0, max=4)]
        data = {'measure' : test_measure}
        response = self.client.post('/restaurants/add_measure/'+ str(id_operator) + '/' + str(restaurant.id), json=data)
        assert response.status_code == 200

    def test_add_avg_stay_400(self):
        response = self.client.post('/restaurants/add_avg_stay/' + str(0) + '/' + str(0), json={})
        assert response.status_code == 400
        restaurant, id_operator, _ = self.add_restaurant()
        response = self.client.post('/restaurants/add_avg_stay/'+ str(id_operator) + '/' + str(restaurant.id), json={})
        assert response.status_code == 400
        json_response = response.json
    
    def test_add_avg_stay_200(self):      
        restaurant, id_operator, _ = self.add_restaurant()
        hours = self.faker.random_int(min=0, max=23)
        minutes = self.faker.random_int(min=1, max=59)
        data = {'hours' : hours,
                'minutes': minutes}
        print("MUSCAAAAAAAAAAAAA")
        response = self.client.post('/restaurants/add_avg_stay/'+ str(id_operator) + '/' + str(restaurant.id), json=data)
        json_response = response.json
        print(json_response)
        assert response.status_code == 200

    def test_post_edit_restaurant_400(self):
        response = self.client.post('edit_restaurant/' + str(0) + '/' + str(0), json={})
        assert response.status_code == 400
        restaurant, id_operator, _ = self.add_restaurant()
        response = self.client.post('edit_restaurant/'+ str(id_operator) + '/' + str(restaurant.id), json={})
        assert response.status_code == 400
        json_response = response.json

    def test_post_edit_restaurant_200(self):
        restaurant, id_operator, data = self.add_restaurant()
        response = self.client.post('edit_restaurant/'+ str(id_operator) + '/' + str(restaurant.id), json=data)
        json_response = response.json
        assert response.status_code == 200

    #Tests on Helper Methods

    def test_toggle_like(self):
        pass

    def test_convert_avg_stay_fromat_0(self):
        from restaurants.resources.restaurants import convert_avg_stay_format
        avg_stay = None
        self.assertEqual(0, convert_avg_stay_format(avg_stay))

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
        self.restaurant_manager.create_restaurant(restaurant)       
        data = {'name': restaurant.name,
                'address': restaurant.address,
                'city':  restaurant.city,
                'phone': restaurant.phone,
                'menu_type': restaurant.menu_type}
        id_operator = self.faker.random_int(min=0, max=50000)
        return restaurant, id_operator, data
