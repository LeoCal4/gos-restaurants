from resources.resource_test import ResourceTest



class RestaurantResTest(ResourceTest):


    def setUpClass(cls):
        super(RestaurantResTest, cls).setUpClass()
        from restaurants.dao.restaurant_manager import RestaurantManager
        cls.restaurant_manager = RestaurantManager
        from tests.models.test_restaurant import TestRestaurant
        cls.test_restaurant = TestRestaurant 
        from tests.models.test_restaurant_availability import TestRestaurantAvailability
        cls.test_availability = TestRestaurantAvailability

    def test_my_restaurant(self):
        pass

    def test_restaurant_sheet(self):
        pass

    def test_like_toggle(self):
        pass

    def test_post_add(self):
        pass

    def test_add_tables(self):
        pass

    def test_add_times(self):
        pass

    def test_add_avg_stay(self):
        pass

    def test_post_edit_restaurant(self):
        pass

    #Tests on Helper Methods

    def test_toggle_like(self):
        pass

    def test_convert_avg_stay_fromat(self):
        pass

    def test_validate_ava(self):
        pass
