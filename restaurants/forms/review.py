import wtforms as f
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange

from restaurants.models.restaurant_rating import RestaurantRating


class ReviewForm(FlaskForm):
    """Form created to allow the customers to insert a new review: an integer value
    along with a comment
    """

    value = f.IntegerField(
        'Rate',
        validators=[NumberRange(
            min=RestaurantRating.MIN_VALUE,
            max=RestaurantRating.MAX_VALUE
        )]
    )

    review = f.TextAreaField(
        'Review',
        validators=[DataRequired()]
    )
