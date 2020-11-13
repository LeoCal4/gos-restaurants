import wtforms as f
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class RestaurantForm(FlaskForm):
    """Form created to allow the operators to add the information about their restaurant
    """

    list_menu = ['Italian', 'Japanese', 'Chinese','Mexican','American', 'Vegan', 'Vegetarian']

    name = f.StringField('Name', validators=[DataRequired()])
    address = f.StringField('Address', validators=[DataRequired()])
    city = f.StringField('City', validators=[DataRequired()])
    phone = f.StringField('Phone', validators=[DataRequired()])
    menu_type = f.SelectField('Menu type', choices=list_menu, default='Italian')

    display = ['name', 'address', 'city', 'phone', 'menu_type']
