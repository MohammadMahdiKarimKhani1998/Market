from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import category_view, product_view, comment_view, like_dislike, CategoryList, BrandList, CategoryBrandList, ProductList, ShopProductList, CommentsList

urlpatterns = [
    path('single/<slug:slug>/<slug:pk>/', product_view, name='product'),
    path('category/<slug:slug>/<int:pk>/', category_view, name='category'),
    path('comment/', comment_view, name='comment'),
    path('like_dislike/', like_dislike, name='like_dislike'),
    path('api/category/', CategoryList.as_view()),
    path('api/brand/', BrandList.as_view()),
    path('api/CategoryBrand/', CategoryBrandList.as_view()),
    path('api/product/', ProductList.as_view()),
    path('api/shop_product/', ShopProductList.as_view()),
    path('api/comments/', CommentsList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
