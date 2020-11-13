import wtforms as f
from flask_wtf import FlaskForm


class RestaurantSearchForm(FlaskForm):
    """Form created to allow the customers search for restaurant depending on
    different fields
    """

    DEFAULT_SEARCH_FILTER = 'Name'
    restaurant_filters = ['Name', 'City', 'Menu Type']
    keyword = f.StringField('Search Field')
    filters = f.SelectField('Search By', choices=restaurant_filters, default=1)
