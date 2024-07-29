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
    delivery_data = {
        "order_id": order_data['id'],
        "user_id": order_data['user_id'],
        "payment_method": order_data['payment_method'],
        "address": order_data['address'],
        "delivery_method": order_data['delivery_method'],
        "items": order_data['items'],  # Include order items here
    }
    publish_message(delivery_data, 'delivery_exchange', 'delivery.created')


@shared_task
def update_inventory(order_data):
    listing_data = {
        "order_id": order_data['id'],
        "user_id": order_data['user_id'],
        "payment_method": order_data['payment_method'],
        "address": order_data['address'],
        "delivery_method": order_data['delivery_method'],
        "items": order_data['items'],  # Include order items here
    }
    publish_message(listing_data, 'listing_exchange', 'listing.updated')