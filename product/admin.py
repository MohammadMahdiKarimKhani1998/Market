from django.contrib import admin
from product.models import Category, Brand, Product, ShopProduct, Comments, Images, CategoryBrand, CommentLike


class CategoryItemAdmin(admin.TabularInline):
    model = Category
    fields = ('slug', 'title')
    extra = 1
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'updated_at')
    list_filter = ('slug', 'title', 'created_at')
    search_fields = ('slug', 'title')
    date_hierarchy = 'updated_at'
    inlines = [CategoryItemAdmin, ]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'updated_at')
    list_filter = ('slug', 'name', 'created_at')
    search_fields = ('slug', 'name')
    date_hierarchy = 'updated_at'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'brand', 'category', 'updated_at')
    list_filter = ('slug', 'name', 'created_at', 'category', 'brand')
    search_fields = ('slug', 'name')
    date_hierarchy = 'updated_at'


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'shop', 'quantity', 'price')
    list_filter = ('product', 'shop')
    search_fields = ('product', 'shop')


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rate')
    list_filter = ('user', 'product')
    search_fields = ('user', 'product')
    date_hierarchy = 'created_at'


@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'created_at')
    list_filter = ('product', )
    search_fields = ('product', )
    date_hierarchy = 'publish_time'


@admin.register(CategoryBrand)
class CategoryBrandAdmin(admin.ModelAdmin):
    list_display = ('category', 'brand')
    list_filter = ('category', 'brand')
    search_fields = ('category', 'brand')


admin.site.register(CommentLike)
