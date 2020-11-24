"""
This file contains all events that can be sent as message
to relative channels.
"""


class Event:
    """
    Base event class
    """

    def __init__(self):
        self.key = None
        self.body = None


class RestaurantDeletion(Event):
    """
    Class that represents the event "Restaurant with *id*=id is deleted".
    """

    def __init__(self, restaurant_id):
        self.key = 'RESTAURANT_DELETION'
        self.body = {
            'restaurant_id': restaurant_id
        }
