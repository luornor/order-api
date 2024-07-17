from django.db import models
# Create your models here.
from django.db import models


class Order(models.Model):
    DELIVERY_CHOICES = [
        ('standard', 'Standard'),
        ('express', 'Express'),
        ('overnight', 'Overnight'),
    ]
    user_id = models.IntegerField()
    listing_id = models.IntegerField()
    delivery_provider = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    address = models.CharField(max_length=255)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='standard')
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[
        ('on_hold', 'On Hold'),
        ('ready', 'Ready'),
        ('on_the_way', 'On the Way'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], default='on_hold')

    def __str__(self):
        return f'{self.user_id}'
