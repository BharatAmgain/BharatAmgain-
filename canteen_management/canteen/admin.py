from django.contrib import admin
from .models import FoodCategory, FoodItem, Order, OrderItem

admin.site.register(FoodCategory)
admin.site.register(FoodItem)
admin.site.register(Order)
admin.site.register(OrderItem)

