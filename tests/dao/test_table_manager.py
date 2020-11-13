import random
from datetime import datetime, timedelta

from faker import Faker

from .dao_test import DaoTest


class TestTableManager(DaoTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestTableManager, cls).setUpClass()
        from tests.models.test_restaurant import TestRestaurant
        cls.test_restaurant = TestRestaurant
        from tests.models.test_table import TestTable
        cls.test_table = TestTable
        from restaurants.dao import table_manager
        from restaurants.models import table

        cls.table_manager = table_manager.TableManager
        from restaurants.dao import restaurant_manager
        cls.restaurant_manager = restaurant_manager.RestaurantManager
        cls.table = table
    
    def test_create_table(self):
        table1, _ = self.test_table.generate_random_table()
        self.table_manager.create_table(table=table1)
        table2 = self.table_manager.retrieve_by_id(id_=table1.id)
        self.test_table.assertEqualTables(table1, table2)

    def test_delete_table(self):
        base_table, _ = self.test_table.generate_random_table()
        self.table_manager.create_table(table=base_table)
        self.table_manager.delete_table(base_table)
        self.assertIsNone(self.table_manager.retrieve_by_id(base_table.id))

    def test_delete_table_by_id(self):
        base_table, _ = self.test_table.generate_random_table()
        self.table_manager.create_table(table=base_table)
        self.table_manager.delete_table_by_id(base_table.id)
        self.assertIsNone(self.table_manager.retrieve_by_id(base_table.id))

    def test_update_table(self):
        base_table, _ = self.test_table.generate_random_table()
        self.table_manager.create_table(table=base_table)
        base_table.set_capacity(random.randint(self.table.Table.MIN_TABLE_CAPACITY, self.table.Table.MAX_TABLE_CAPACITY))
        updated_table = self.table_manager.retrieve_by_id(id_=base_table.id)
        self.test_table.assertEqualTables(base_table, updated_table)
    
    def test_multiple_tables_retrieved_by_restaurant_id(self):
        base_tables = []
        restaurant, _ = self.test_restaurant.generate_random_restaurant()
        for _ in range(random.randint(2, 10)):
            table, _ = self.test_table.generate_random_table()
            base_tables.append(table)
            table.restaurant = restaurant
        self.restaurant_manager.create_restaurant(restaurant=restaurant)
        for table in base_tables:
            self.table_manager.create_table(table=table)
        retrieved_tables = self.table_manager.retrieve_by_restaurant_id(restaurant_id=restaurant.id)
        for base_table, retrieved_table in zip(base_tables, retrieved_tables):
            self.test_table.assertEqualTables(base_table, retrieved_table)
