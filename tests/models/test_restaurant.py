import random
import string
import unittest

from faker import Faker

from .model_test import ModelTest


class TestRestaurant(ModelTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestRestaurant, cls).setUpClass()

        from restaurants.models import restaurant
        cls.restaurant = restaurant

    @staticmethod
    def generate_random_restaurant():
        from restaurants.models.restaurant import Restaurant

        name = TestRestaurant.faker.company()
        address = TestRestaurant.faker.street_address()
        city = TestRestaurant.faker.city()
        lat = TestRestaurant.faker.latitude()
        lon = TestRestaurant.faker.longitude()
        phone = TestRestaurant.faker.phone_number()
        menu_type = TestRestaurant.faker.country()

        restaurant = Restaurant(
            name=name,
            address=address,
            city=city,
            lat=lat,
            lon=lon,
            phone=phone,
            menu_type=menu_type
        )

        return restaurant, (name, address, city, lat, lon, phone, menu_type)

    @staticmethod
    def assertEqualRestaurants(r1, r2):
        t = unittest.FunctionTestCase(TestRestaurant)
        t.assertEqual(r1.name, r2.name)
        t.assertEqual(r1.address, r2.address)
        t.assertEqual(r1.city, r2.city)
        t.assertEqual(r1.lat, r2.lat)
        t.assertEqual(r1.lon, r2.lon)
        t.assertEqual(r1.phone, r2.phone)
        t.assertEqual(r1.menu_type, r2.menu_type)

    def test_rest_init(self):
        for _ in range(0, 10):
            restaurant, (name, address, city, lat, lon, phone, menu_type) = TestRestaurant.generate_random_restaurant()

            self.assertEqual(restaurant.name, name)
            self.assertEqual(restaurant.address, address)
            self.assertEqual(restaurant.city, city)
            self.assertEqual(restaurant.lat, lat)
            self.assertEqual(restaurant.lon, lon)
            self.assertEqual(restaurant.phone, phone)
            self.assertEqual(restaurant.menu_type, menu_type)

    def test_valid_name(self):
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        name = TestRestaurant.faker.company()
        restaurant.set_name(name)
        self.assertEqual(restaurant.name, name)

    def test_long_name(self):
        long_name = ''.join(
            random.choice(string.ascii_letters) for _ in
            range(0, self.restaurant.Restaurant.MAX_STRING_LENGTH + random.randint(1, 100))
        )

        restaurant, _ = TestRestaurant.generate_random_restaurant()
        with self.assertRaises(ValueError):
            restaurant.set_name(long_name)

    def test_short_name(self):
        short_name = ""
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        with self.assertRaises(ValueError):
            restaurant.set_name(short_name)
    
    def test_valid_address(self):
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        address = TestRestaurant.faker.street_address()
        restaurant.set_address(address)
        self.assertEqual(restaurant.address, address)

    def test_long_address(self):
        long_name = ''.join(
            random.choice(string.ascii_letters) for _ in
            range(0, self.restaurant.Restaurant.MAX_STRING_LENGTH + random.randint(1, 100))
        )
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        with self.assertRaises(ValueError):
            restaurant.set_address(long_name)
    
    def test_short_address(self):
        short_name = ''
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        with self.assertRaises(ValueError):
            restaurant.set_address(short_name)

    def test_valid_city(self):
        city = TestRestaurant.faker.city()
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        restaurant.set_city(city)
        self.assertEqual(restaurant.city, city)

    def test_long_city(self):
        long_name = ''.join(
            random.choice(string.ascii_letters) for _ in
            range(0, self.restaurant.Restaurant.MAX_STRING_LENGTH + random.randint(1, 100))
        )
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        with self.assertRaises(ValueError):
            restaurant.set_city(long_name)
    
    def test_short_city(self):
        short_name = ''
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        with self.assertRaises(ValueError):
            restaurant.set_city(short_name)

    def test_valid_lat(self):
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        lat = TestRestaurant.faker.latitude()
        restaurant.set_lat(lat)
        self.assertEqual(restaurant.lat, lat)

    def test_too_high_lat1(self):
        lat = self.restaurant.Restaurant.MAX_LAT + random.randint(1, 100)
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        with self.assertRaises(ValueError):
            restaurant.set_lat(lat)

    def test_too_low_lat1(self):
        lat = self.restaurant.Restaurant.MIN_LAT - random.randint(1, 100)
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        with self.assertRaises(ValueError):
            restaurant.set_lat(lat)

    def test_valid_lon(self):
        lon = TestRestaurant.faker.longitude()
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        restaurant.set_lon(lon)
        self.assertEqual(restaurant.lon, lon)

    def test_too_high_lon1(self):
        lon = self.restaurant.Restaurant.MAX_LON + random.randint(1, 100)
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        with self.assertRaises(ValueError):
            restaurant.set_lon(lon)

    def test_too_low_lon1(self):
        lon = self.restaurant.Restaurant.MIN_LON - random.randint(1, 100)
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        with self.assertRaises(ValueError):
            restaurant.set_lon(lon)

    def test_valid_phone(self):
        phone = TestRestaurant.faker.phone_number()
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        restaurant.set_phone(phone)
        self.assertEqual(restaurant.phone, phone)

    def test_too_high_phone1(self):
        restaurant, _ = TestRestaurant.generate_random_restaurant()

        phone = ''.join(['%s' % i for i in range(0, self.restaurant.Restaurant.MAX_PHONE_LEN + 1)])
        with self.assertRaises(ValueError):
            restaurant.set_phone(phone)

    def test_too_short_phone(self):
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        with self.assertRaises(ValueError):
            phone = ""
            restaurant.set_phone(phone)

    def test_valid_menu_type(self):
        menu_type = TestRestaurant.faker.country()
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        restaurant.set_menu_type(menu_type)
        self.assertEqual(restaurant.menu_type, menu_type)

    def test_long_menu_type(self):
        long_name = ''.join(
            random.choice(string.ascii_letters) for _ in
            range(0, self.restaurant.Restaurant.MAX_STRING_LENGTH + random.randint(1, 100))
        )

        restaurant, _ = TestRestaurant.generate_random_restaurant()
        with self.assertRaises(ValueError):
            restaurant.set_menu_type(long_name)

    def test_short_menu_type(self):
        short_name = ""
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        with self.assertRaises(ValueError):
            restaurant.set_menu_type(short_name)

    def test_is_open_default(self):
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        self.assertEqual(restaurant.is_open, True)

    def test_is_open_false(self):
        restaurant, _ = TestRestaurant.generate_random_restaurant()
        restaurant.set_is_open(False)
        self.assertEqual(restaurant.is_open, False)

    def test_is_open_true(self):
        import datetime

        restaurant, _ = TestRestaurant.generate_random_restaurant()
        restaurant.set_is_open(True)
        self.assertEqual(restaurant.is_open, True)
        self.assertEqual(restaurant.is_open_date(when=datetime.datetime(1999, 10, 12, 10, 22, 11)), False)
