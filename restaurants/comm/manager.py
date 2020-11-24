from restaurants.comm import rabbit, disabled
from restaurants.comm.events import *


class EventManager(object):
    """This class is the event manager of system.
    It handles all events that application can trigger.

    Each method inside this class will send a message to message broker.
    """

    @classmethod
    def _send_message(cls, event: Event):
        """
        Send a message to broker.

        :param event: event to be sent
        :return: None
        """
        if disabled:
            return

        rabbit.send(
            body=event.body,
            routing_key=event.key
        )

    @classmethod
    def restaurant_deleted(cls, restaurant_id):
        """
        Trigger the event restaurant_deleted.

        :param restaurant_id: the id of restaurant
        :return: None
        """
        event = RestaurantDeletion(restaurant_id=restaurant_id)
        cls._send_message(event)
