import unittest


class ModelTest(unittest.TestCase):
    """
    This class should be implemented by
    all classes that tests models
    """
    @classmethod
    def setUpClass(cls):
        from restaurants import create_app
        create_app()
