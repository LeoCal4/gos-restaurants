from restaurants import app
from kombu.mixins import ConsumerMixin
from kombu import Exchange, Queue


class CustomerDeletionWorker(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection

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
        """
        @TODO: delete the related restaurant
        """

    def get_consumers(self, consumer, channel):
        return [consumer(queues=self.queues,
                         callbacks=[self.on_message])]
