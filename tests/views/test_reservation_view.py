from flask import url_for
from faker import Faker
import datetime

from tests.models.test_reservation import TestReservation
from tests.models.test_customer import TestCustomer
from tests.models.test_table import TestTable
from tests.models.test_restaurant_availability import TestRestaurantAvailability


from tests.views.view_test import ViewTest


class TestReservationView(ViewTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestReservationView, cls).setUpClass()

        from restaurants.views import reservation
        from restaurants.views import home

        from restaurants.dao import reservation_manager, customer_manager, restaurant_manager
        from restaurants.dao import restaurant_availability_manager, table_manager
        
        cls.reservation_manager = reservation_manager.ReservationManager
        cls.customer_manager = customer_manager.CustomerManager
        cls.restaurant_manager = restaurant_manager.RestaurantManager
        cls.ava_manager = restaurant_availability_manager.RestaurantAvailabilityManager
        cls.table_manager = table_manager.TableManager

        from tests.models import test_restaurant
        cls.restaurant_test = test_restaurant.TestRestaurant




    """def test_create_reservation(self):
        from restaurants.models import Restaurant, Table, RestaurantAvailability
        self.login_test_customer()
        restaurant, _ = self.restaurant_test.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        table = Table(4, restaurant)
        self.table_manager.create_table(table)
        start_ava = datetime.time(hour=8)
        end_ava = datetime.time(hour=16)
        ava = RestaurantAvailability(restaurant.id, 'Monday', start_time=start_ava, end_time=end_ava)
        self.ava_manager.create_availability(ava)
        rv = self.client.get('/create_reservation/' + str(restaurant.id), follow_redirects=True)
        assert rv.status_code == 200
        self.login_test_operator()
        rv = self.client.get('/create_reservation/' + str(restaurant.id), follow_redirects=True)
        assert rv.status_code == 200
        self.login_test_customer()
        start_date = datetime.date(year=2020, month=11, day=9)
        start_time = datetime.time(hour=13, minute=30)
        data = dict(start_date=start_date, start_time=start_time,people_number=1)
        rv = self.client.post('/create_reservation/' + str(restaurant.id), 
                            data=data, 
                            follow_redirects=True
                            )
        assert rv.status_code == 200
        start_date = datetime.date(year=2020, month=11, day=9)
        start_time = datetime.time(hour=19, minute=30)
        data = dict(start_date=start_date, start_time=start_time,people_number=1)
        rv = self.client.post('/create_reservation/' + str(restaurant.id), 
                            data=data, 
                            follow_redirects=True
                            )
        assert rv.status_code == 200

        start_date = datetime.date(year=2020, month=11, day=9)
        start_time = datetime.time(hour=12, minute=30)
        data = dict(start_date=start_date, start_time=start_time,people_number=50)
        rv = self.client.post('/create_reservation/' + str(restaurant.id), 
                            data=data, 
                            follow_redirects=True
                            )
        assert rv.status_code == 200"""

    def test_check_time_interval(self):
        from restaurants.views.reservation import check_time_interval
        start1 = datetime.datetime(year=2020, month=11, day=9)
        end1 = datetime.datetime(year=2020, month=11, day=15)
        start2 = datetime.datetime(year=2020, month=11, day=20)
        end2 = datetime.datetime(year=2020, month=11, day=22)
        self.assertFalse(check_time_interval(start1, end1, start2, end2))

        start2 = datetime.datetime(year=2020, month=11, day=8)
        end2 = datetime.datetime(year=2020, month=11, day=11)
        self.assertTrue(check_time_interval(start1, end1, start2, end2))

        start2 = datetime.datetime(year=2020, month=11, day=12)
        end2 = datetime.datetime(year=2020, month=11, day=25)
        self.assertTrue(check_time_interval(start1, end1, start2, end2))

    def test_check_time_interval(self):
        from restaurants.models import Restaurant, Table, RestaurantAvailability
        from restaurants.views.reservation import check_rest_ava
        self.login_test_customer()
        restaurant, _ = self.restaurant_test.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        start_ava = datetime.time(hour=1)
        end_ava = datetime.time(hour=23)
        ava = RestaurantAvailability(restaurant.id, 'Monday', start_time=start_ava, end_time=end_ava)
        self.ava_manager.create_availability(ava)
        start1 = datetime.datetime(year=2020, month=11, day=9, hour=10)
        end1 = datetime.datetime(year=2020, month=11, day=9, hour=13)
        self.assertTrue(check_rest_ava(restaurant, start1, end1))
        start1 = datetime.datetime(year=2020, month=11, day=10, hour=10)
        end1 = datetime.datetime(year=2020, month=11, day=10, hour=13)
        self.assertFalse(check_rest_ava(restaurant, start1, end1))


    def test_customer_my_reservation(self):
        rv = self.client.get('/customer/my_reservations')
        assert rv.status_code == 200

    def test_confirm_reservation(self):
        self.login_test_customer()
        reservation,_ = TestReservation.generate_random_reservation()
        self.reservation_manager.create_reservation(reservation)
        rv = self.client.get('/reservation/confirm/' + str(reservation.id), follow_redirects=True)
        assert rv.status_code == 200
    
    def test_edit_reservation(self):
        customer = self.login_test_customer()
        reservation,_ = TestReservation.generate_random_reservation(user=customer)
        self.reservation_manager.create_reservation(reservation)
        rv = self.client.get('/edit/' + str(reservation.id) +'/'+ str(customer.id),follow_redirects=True)
        assert rv.status_code == 200

    def test_delete_reservation_customer(self):
        customer = self.login_test_customer()
        reservation,_ = TestReservation.generate_random_reservation()
        self.reservation_manager.create_reservation(reservation)
        rv = self.client.get('/delete/'+ str(reservation.id) +'/'+ str(customer.id),follow_redirects=True)
        assert rv.status_code == 200
    
    def test_delete_reservation(self):
        customer = self.login_test_customer()
        restaurant,_ = self.restaurant_test.generate_random_restaurant()
        self.restaurant_manager.create_restaurant(restaurant)
        reservation,_ = TestReservation.generate_random_reservation(restaurant=restaurant)
        self.reservation_manager.create_reservation(reservation)
        rv = self.client.get('/delete/'+ str(reservation.id) +'/'+ str(customer.id),follow_redirects=True)
        assert rv.status_code == 200
    
    def test_reservation_all(self):
        customer = self.login_test_customer()
        restaurant,_ = self.restaurant_test.generate_random_restaurant()
        rv = self.client.get('/reservations/'+ str(restaurant.id))
        assert rv.status_code == 200