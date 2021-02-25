from rest_framework import serializers

from product.models import Category, Brand, CategoryBrand, Comments


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title', 'image', 'detail', 'created_at', 'updated_at']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'slug', 'name', 'image', 'detail', 'created_at', 'updated_at']


class CategoryBrandSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.title')
    brand = serializers.ReadOnlyField(source='brand.name')

    class Meta:
        model = CategoryBrand
        fields = ['id', 'category', 'brand']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.title')
    brand = serializers.ReadOnlyField(source='brand.name')

    class Meta:
        model = Brand
        fields = ['id', 'slug', 'name', 'image', 'detail', 'created_at', 'updated_at', 'category', 'brand']


class ShopProductSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='product.id')
    shop = serializers.ReadOnlyField(source='shop.slug')

    class Meta:
        model = CategoryBrand
        fields = ['id', 'price', 'quantity', 'shop', 'product']


class CommentsSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='product.id')
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Comments
        fields = ['id', 'content', 'rate', 'created_at', 'product', 'user']
