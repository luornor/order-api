from django.db import models


class Cart(models.Model):
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart {self.id} for User {self.user_id}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    listing_id = models.IntegerField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Item {self.id} in Cart {self.cart_id}'


class Order(models.Model):
    DELIVERY_CHOICES = [
        ('standard', 'Standard'),
        ('express', 'Express'),
        ('overnight', 'Overnight'),
    ]
    PAYMENT_CHOICES = [
        ('momo', 'Momo'),
        ('cash', 'Cash'),
    ]
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255,choices=PAYMENT_CHOICES, default='cash')
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
        return f'Order {self.id} by User {self.user_id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    listing_id = models.IntegerField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Item {self.id} in Order {self.order_id}'
