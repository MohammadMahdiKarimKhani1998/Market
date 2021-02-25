from django.contrib import admin
from order.models import Order, Basket, Payment, OrderItem, BasketItems


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    extra = 1
    show_change_link = True


class BasketItemAdmin(admin.TabularInline):
    model = BasketItems
    extra = 1
    show_change_link = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    list_filter = ('user',)
    search_fields = ('user',)
    date_hierarchy = 'updated_at'
    inlines = [OrderItemAdmin, ]


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('user',)
    search_fields = ('user',)
    inlines = [BasketItemAdmin, ]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'amount')
    list_filter = ('user', 'order')
    search_fields = ('order', 'user')
