from django.contrib import admin
from .models import User, Manager, DeliveryCrew, Category, MenuItem, Cart, Order, OrderItem, Testimonial

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'address', 'phone_number', 'is_manager', 'is_delivery_crew')
    search_fields = ('username', 'email')

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(DeliveryCrew)
class DeliveryCrewAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'featured', 'description')
    list_filter = ('category', 'featured')
    search_fields = ('title',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'menuitem', 'quantity', 'unit_price', 'price')
    list_filter = ('user',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'delivery_crew', 'status', 'total', 'date')
    list_filter = ('status', 'date')
    search_fields = ('user__username',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menuitem', 'quantity', 'unit_price', 'price')
    list_filter = ('order', 'menuitem')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'date_created')
    search_fields = ('user__username', 'text')
