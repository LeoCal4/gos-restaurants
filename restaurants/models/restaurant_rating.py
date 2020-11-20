import datetime

import timeago
from restaurants import db
from sqlalchemy.orm import relationship


class RestaurantRating(db.Model):
    MIN_VALUE = 0
    MAX_VALUE = 10

    __tablename__ = 'RestaurantRating'

    REVIEW_MAX_LENGTH = 200

    customer_id = db.Column(
        db.Integer,
        primary_key=True
    )

    restaurant_id = db.Column(
        db.Integer,
        db.ForeignKey('Restaurant.id'),
        primary_key=True
    )

    restaurant = relationship('Restaurant', back_populates='ratings')

    value = db.Column(
        db.Integer,
        nullable=False
    )

    review = db.Column(
        db.String(
            length=REVIEW_MAX_LENGTH,
        ),
        nullable=True
    )

    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, customer_id, restaurant_id, customer_name, value, review=None):
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.customer_name = customer_name
        self.value = value[0] if type(value) == tuple else value # for some unknown reason value is a tuple (sometimes)
        self.review = review

    @staticmethod
    def check_value(value: int):
        if value < RestaurantRating.MIN_VALUE or value > RestaurantRating.MAX_VALUE:
            raise ValueError('Invalid value for rating!')

    @staticmethod
    def check_review(review: str):
        if len(review) > RestaurantRating.REVIEW_MAX_LENGTH:
            raise ValueError('Review\'s length must not be greater than MAX_SIZE')

    def set_value(self, value):
        RestaurantRating.check_value(value)
        self.value = value

    def set_review(self, review):
        RestaurantRating.check_review(review)
        self.review = review

    def get_how_long_ago(self):
        return timeago.format(datetime.datetime.now(), self.timestamp)

    def serialize(self):
        att_dict = dict([(k,v) for k,v in self.__dict__.items() if k[0] != '_'])
        att_dict['timestamp'] = self.get_how_long_ago()
        return att_dict
