from rest_framework import serializers

from order.models import BasketItems


class BasketItemsSerializer(serializers.ModelSerializer):
    basket = serializers.ReadOnlyField(source="basket.user.email")
    shop_product = serializers.ReadOnlyField(source="shop_product.product.id")

    class Meta:
        model = BasketItems
        fields = ['id', 'count', 'price', 'basket', 'shop_product']
