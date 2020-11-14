from sqlalchemy.orm import relationship

from restaurants import db


class Table(db.Model):
    __tablename__ = 'Table'

    MIN_TABLE_CAPACITY = 1
    MAX_TABLE_CAPACITY = 15

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('Restaurant.id', ondelete="CASCADE"))
    restaurant = relationship('Restaurant', back_populates="tables")
    capacity = db.Column(db.Integer)
    
    def serialize(self):
        return dict([(k,v) for k,v in self.__dict__.items() if k[0] != '_'])

    def __init__(self, capacity, restaurant):
        self.capacity = capacity
        self.restaurant = restaurant

    def set_capacity(self, capacity):
        if capacity < self.MIN_TABLE_CAPACITY or capacity > self.MAX_TABLE_CAPACITY:
            raise ValueError('You can\'t set a negative value, zero or greater than '
                             + str(self.MAX_TABLE_CAPACITY))
        self.capacity = capacity

    def set_restaurant(self, restaurant):
        self.restaurant = restaurant
