from django.db import models
# Create your models here.
from django.db import models


class Order(models.Model):
    user_id = models.IntegerField()
    listing_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    address = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], default='pending')

    def __str__(self):
        return f'{self.user_id}'
