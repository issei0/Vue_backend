from ast import Or
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserConfig(UserAdmin):
    model = User
    search_fields = ('email', 'username',)
    list_filter = ('email', 'username', 'is_active', 'is_staff')
    ordering = ('-date_joined',)
    list_display = ('id', 'email', 'username', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'username', 'email', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'username', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
admin.site.register(User, UserConfig),
admin.site.register(Category),
class ProductConfig(admin.ModelAdmin):
    model = Product
    search_fields = ('name',)
    list_filter = ('category',)
    list_display = ('name', 'category', 'price')
admin.site.register(Product, ProductConfig),
class OrderConfig(admin.ModelAdmin):
    model = Order
    search_fields = ('email', 'username', 'phone_number')
    list_display = ('username', 'email', 'phone_number', 'paid_amount')
admin.site.register(Order, OrderConfig),
class OrderItemConfig(admin.ModelAdmin):
    model = OrderItem
    search_fields = ('product', 'quantity')
admin.site.register(OrderItem, OrderItemConfig)