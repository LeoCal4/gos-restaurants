import unittest


class ViewTest(unittest.TestCase):
    """
    This class should be implemented by
    all classes that tests views
    """
    client = None

    @classmethod
    def setUpClass(cls):
        from restaurants import create_app
        app = create_app()
        cls.client = app.test_client()
        from tests.models.test_customer import TestCustomer
        cls.test_customer = TestCustomer
        from restaurants.dao import customer_manager
        cls.customer_manager = customer_manager.CustomerManager
        from tests.models.test_operator import TestOperator
        cls.test_operator = TestOperator
        from restaurants.dao import operator_manager
        cls.operator_manager = operator_manager.OperatorManager
        from tests.models.test_authority import TestAuthority
        cls.test_authority = TestAuthority
        from restaurants.dao import health_authority_manager
        cls.authority_manager = health_authority_manager.AuthorityManager

    def login_test_customer(self):
        """
        Simulate the customer login for testing the views with # @login_required
        :return: customer
        """
        customer, _ = self.test_customer.generate_random_customer()
        psw = customer.password
        customer.set_password(customer.password)
        self.customer_manager.create_customer(customer=customer)
        data = {'email': customer.email, 'password': psw}
        assert self.client.post('/login', data=data, follow_redirects=True).status_code == 200
        return customer

    def login_test_operator(self):
        """
        Simulate the operator login for testing the views with # @login_required
        :return: operator
        """
        operator, _ = self.test_operator.generate_random_operator()
        psw = operator.password
        operator.set_password(operator.password)
        self.operator_manager.create_operator(operator=operator)
        data = {'email': operator.email, 'password': psw}
        assert self.client.post('/login', data=data, follow_redirects=True).status_code == 200
        return operator

    def login_test_authority(self):
        """
        Simulate the authority login for testing the views with # @login_required
        :return: authority
        """
        authority, _ = self.test_authority.generate_random_authority()
        psw = authority.password
        authority.set_password(authority.password)
        self.authority_manager.create_authority(authority=authority)
        data = {'email': authority.email, 'password': psw}
        assert self.client.post('/login', data=data, follow_redirects=True).status_code == 200
        return authority
