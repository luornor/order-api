from __future__ import absolute_import, unicode_literals

import os
from celery import Celery, bootsteps
from kombu import Exchange, Queue, Consumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'order_api.settings')

app = Celery('order_api')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# Namespace 'CELERY' means all celery-related configuration keys
# should have a 'CELERY_' prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# setting publisher
with app.pool.acquire(block=True) as conn:
    exchange = Exchange(
        name='delivery_exchange',
        type='direct',
        durable=True,
        channel=conn,
    )
    exchange.declare()

    queue = Queue(
        name='delivery_queue',
        exchange=exchange,
        routing_key='delivery.created',
        channel=conn,
        message_ttl=600,
        queue_arguments={
            'x-queue-type': 'classic'
        },
        durable=True
    )
    queue.declare()

# Define custom consumer step for handling messages
class MyConsumerStep(bootsteps.ConsumerStep):

    def get_consumers(self, channel):
        # Define multiple queues
        delivery_queue = Queue('delivery.created', Exchange('delivery_exchange', type='direct'), routing_key='delivery.created')
        listing_queue = Queue('listing.updated', Exchange('listing_exchange', type='direct'), routing_key='listing.updated')

        return [
            Consumer(channel,
                     queues=[delivery_queue],
                     callbacks=[self.handle_delivery_message],
                     accept=['json']),
            Consumer(channel,
                     queues=[listing_queue],
                     callbacks=[self.handle_listing_message],
                     accept=['json'])
        ]

    def handle_delivery_message(self, body, message):
        print('Received delivery message: {0!r}'.format(body))
        # Add your handling logic for delivery messages here
        message.ack()

    def handle_listing_message(self, body, message):
        print('Received listing message: {0!r}'.format(body))
        # Add your handling logic for listing messages here
        message.ack()

app.steps['consumer'].add(MyConsumerStep)