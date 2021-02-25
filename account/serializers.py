from rest_framework import serializers

from account.models import User, Address, Shop


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
