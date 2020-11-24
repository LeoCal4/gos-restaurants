from restaurants import app
from kombu.mixins import ConsumerMixin
from kombu import Exchange, Queue
import json


class OperatorDeletionWorker(ConsumerMixin):
    def __init__(self, connection, logger):
        self.connection = connection
        self.logger = logger

        exchange = Exchange(
            app.config.get('RABMQ_SEND_EXCHANGE_NAME'),
            type='topic',
            channel=connection.channel()
        )

        exchange.declare(nowait=False)
        self.queues = [Queue('RestaurantDeletionQueue', exchange, routing_key='OPERATOR_DELETION')]

    def on_message(self, body, message):
        message.ack()
        app.logger.info('Received a message of user deletion.')
        print(body)
        
        try:
            message_object = json.loads(message)
        except ValueError:
            self.logger.error('Cannot decode json message! Message=%s' % body)
            message.ack()
            return
        
        if 'user_id' not in message_object:
            self.logger.error('Message does not contain user_id!')
        else:
            self.logger.info('Received a message of user deletion with user_id=%s', message_object['user_id'])
            from restaurants.dao.restaurant_manager import RestaurantManager
            try:
                RestaurantManager.delete_restaurant_by_operator_id(op_id=message_object['user_id'])
            except Exception as re:
                self.logger.error('Runtime error during deleting restaurant by operator_id, %s' % re)

        # send ack to message
        message.ack()        

    def get_consumers(self, consumer, channel):
        return [consumer(queues=self.queues,
                         callbacks=[self.on_message])]
