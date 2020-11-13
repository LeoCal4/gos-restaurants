# How write tests for GoOutSafe

Due to Flask initialization issue, we have to write
a setup method for all unittest.TestCase classes.

The following example represents a very simple 
design pattern to be used when you write test cases.


```python
import unittest

class TestMyClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from restaurants import create_app
        create_app('config.TestConfig')

        '''
            now you can import all 
            objects you need for testing,
            and set it as class properties
        '''
        from restaurants.models import restaurant
        cls.restaurant = restaurant

    def test_restaurant(self):
        rest = self.restaurant.Restaurant()
        # test it
``` 

In this way we fix the issue by executing the Flask initialization code in the setUpClass method, that is executed once before the execution of the tests in the class.

