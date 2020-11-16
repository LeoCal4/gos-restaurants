import unittest
from datetime import datetime, timedelta

from faker import Faker

from .model_test import ModelTest


class TestTable(ModelTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestTable, cls).setUpClass()
        from restaurants.models import restaurant, table
        cls.table = table
        cls.restaurant = restaurant
        from .test_restaurant import TestRestaurant
        cls.test_restaurant = TestRestaurant

    @staticmethod
    def generate_random_table(fixed_restaurant=None):
        from restaurants.models.table import Table
        capacity = TestTable.faker.random_int(min=1,max=15)
        if fixed_restaurant is None:
            test_table = TestTable()
            test_table.setUpClass()
            restaurant, _ = test_table.test_restaurant.generate_random_restaurant()
        else:
            restaurant = fixed_restaurant

        table = Table(capacity=capacity, restaurant=restaurant)

        return table, (capacity, restaurant)

    @staticmethod
    def assertEqualTables(t1, t2):
        t = unittest.FunctionTestCase(TestTable)
        t.assertEqual(t1.capacity, t2.capacity)
        t.assertEqual(t1.restaurant.id, t2.restaurant.id)

    def test_table_init(self):
        table, (capacity, restaurant) = TestTable.generate_random_table()
        self.assertEqual(table.capacity, capacity)
        self.assertEqual(table.restaurant.name, restaurant.name)

    def test_set_capacity(self):
        wrong_capacity = TestTable.faker.random_int(min=50)
        table, _ = TestTable.generate_random_table()
        with self.assertRaises(ValueError):
            table.set_capacity(wrong_capacity)
        