"""
This package contains all the classes
that manage the communications with other microservices.

*In particular the behavior of a communication object should be designed as a Signal Sender / Signal Handler*

For example if a user is deleted we should send a message to channel USER with topic = USER_DELETION,
and message = USER WITH ID <USER_ID> DELETED.
The microservice Restaurant, that is subscribed to the channel USER, will filter the messages with USER_DELETION topic.
When it receives a message, it will delete the restaurant associated with foreign key OPERATOR_ID=<USER_ID>.
The same operation can be done by Notification microservice.

Using this kind of design we improve the microservices independence.
"""
import os
from flask_rabmq import RabbitMQ

__REQUIRED_CONFIG_KEYS = ['RABBIT_MQ_HOST', 'RABBIT_MQ_PORT',
                          'RABBIT_MQ_VHOST', 'RABBIT_MQ_SEND_EXCHANGE_NAME']

"""Rabbit MQ instance
"""
rabbit = None
disabled = False


def init_rabbit_conf(app):
    """
    Initialize Rabbit MQ
    :param app: Flask application
    :return: None
    """
    global rabbit

    app.config.setdefault('RABMQ_SEND_POOL_SIZE', 2)
    app.config.setdefault('RABMQ_SEND_POOL_ACQUIRE_TIMEOUT', 5)
    # setting the fanout type to indicate
    # the publish/subscribe design, as documented
    # here https://www.rabbitmq.com/tutorials/tutorial-three-python.html
    #
    app.config.setdefault('RABMQ_SEND_EXCHANGE_TYPE', 'topic')

    # loading configuration
    conf = dict()
    for key in __REQUIRED_CONFIG_KEYS:
        value = os.getenv(key, None)

        if value is None:
            raise RuntimeError('Cannot find the environment variable %s for Rabbit MQ Configuration' % key)

        conf[key] = value

    # Setting up the RabbitURI
    app.config.setdefault('RABMQ_RABBITMQ_URL', 'amqp://%s:%s/%s' % (
        conf['RABBIT_MQ_HOST'], conf['RABBIT_MQ_PORT'],
        conf['RABBIT_MQ_VHOST']))
    app.config.setdefault('RABMQ_SEND_EXCHANGE_NAME', conf['RABBIT_MQ_SEND_EXCHANGE_NAME'])


def init_rabbit_mq(app):
    """
    Create a new instance of Flask RabbitMQ
    """
    global rabbit

    rabbit = RabbitMQ(app=app)

