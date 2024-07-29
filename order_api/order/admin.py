from django.contrib import admin
from .models import Order,CartItem,Cart,OrderItem
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'address', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['user_id','address']



admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)

