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
