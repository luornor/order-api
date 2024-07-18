from __future__ import absolute_import, unicode_literals

from celery import shared_task
from order_api.celery import app


@shared_task
def publish_message(message, exchange_name, routing_key):
    with app.producer_pool.acquire(block=True) as producer:
        producer.publish(
            message,
            exchange=exchange_name,
            routing_key=routing_key,
        )

@shared_task
def send_to_delivery_service(order_data):
    publish_message(order_data, 'delivery_exchange', 'delivery.created')


@shared_task
def update_inventory(order_data):
    publish_message(order_data, 'listing_exchange', 'listing.updated')