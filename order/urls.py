from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import BasketView, add_product_to_basket, edit_table, add_address, BasketItemsList

urlpatterns = [
    path('basket/', BasketView.as_view(), name='basket'),
    path('add_product_to_basket/', add_product_to_basket, name='add_product_to_basket'),
    path('edit_table/', edit_table, name='edit_table'),
    path('basket/add_address/', add_address, name='address'),
    path('api/basket_items/', BasketItemsList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
