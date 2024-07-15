from django.contrib import admin
from .models import Order
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'listing_id', 'quantity', 'address', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['user_id', 'listing_id', 'address']

admin.site.register(Order, OrderAdmin)

