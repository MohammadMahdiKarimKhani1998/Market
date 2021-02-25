import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions

from product.models import Product, Category, ShopProduct, Comments, CommentLike, Brand, CategoryBrand

from django.core.paginator import Paginator

from product.permissions import IsOwnerOrReadOnly
from product.serializers import CategorySerializer, BrandSerializer, CategoryBrandSerializer, ProductSerializer, \
    ShopProductSerializer, CommentsSerializer


def product_view(request, slug, pk):
    product = Product.objects.get(slug=slug)
    product_shop = product.shop_product(pk)
    shops = ShopProduct.objects.filter(product=product)
    category_list = Category.objects.all()
    comments = Comments.objects.filter(product=product).order_by('-created_at')

    context = {
        'product': product,
        'product_shop': product_shop,
        'shops': shops,
        'category_list': category_list,
        'comments': comments
    }
    return render(request, 'product/product.html', context)


@csrf_exempt
def category_view(request, slug, pk):
    category_list = Category.objects.all()
    category = Category.objects.get(slug=slug)

    try:
        if request.body:
            data = json.loads(request.body)
            response = {}
            for ids in data['cache_ids']:
                if int(ids) <= int(data['min']):
                    response[ids] = ids

            for ids in data['cache_ids']:
                if int(ids) >= int(data['max']):
                    response[ids] = ids
            return HttpResponse(json.dumps(response), status=201)

        products = Paginator(category.product(), 4)

        if products.num_pages == 1:
            num_range = [1]
        elif products.num_pages == 2:
            num_range = [1, 2]
        elif pk == 1:
            num_range = [1, 2, 3]
        elif pk == products.num_pages:
            num_range = [pk - 2, pk - 1, pk]
        else:
            num_range = [pk - 1, pk, pk + 1]
        context = {
            'category_list': category_list,
            'category': category,
            'product_filter': products.page(pk),
            'num_pages': num_range,
            'num': products.num_pages,
            'pk': pk
        }
        return render(request, 'product/category.html', context)
    except:
        return render(request, 'home/404.html', )


@csrf_exempt
def like_dislike(request):
    data = json.loads(request.body)
    user = request.user
    comment = Comments.objects.get(id=data['comment_id'])
    status = data['status']
    try:
        if user in comment.comment_likes['users']:
            comment_like = CommentLike.objects.get(comment=comment, user=user)
            comment_like.status = status
            comment_like.save()
            response = {'like_num': comment.like_count, 'dislike_num': comment.dislike_count,
                        "comment_id": comment.id}
            return HttpResponse(json.dumps(response), status=201)
        else:
            CommentLike.objects.create(status=status, user=user, comment=comment)
            response = {'like_num': comment.like_count, 'dislike_num': comment.dislike_count, "comment_id": comment.id}
            return HttpResponse(json.dumps(response), status=201)
    except:
        response = {"error": "error"}
        return HttpResponse(json.dumps(response), status=400)


@csrf_exempt
def comment_view(request):
    data = json.loads(request.body)
    user = request.user
    try:
        comment = Comments.objects.create(product=Product.objects.get(slug=data['product']), content=data['content'],
                                          user=user, rate=data['rate'])
        response = {"content": comment.content, "created_at": str(comment.created_at),
                    "user": comment.user.email, "comment_id": comment.id, 'like_num': comment.like_count,
                    'dislike_num': comment.dislike_count, "image": str(comment.user.image), "rate": comment.rate}
        return HttpResponse(json.dumps(response), status=201)
    except:
        response = {"error": "error"}
        return HttpResponse(json.dumps(response), status=400)


# rest
class CategoryList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryBrandList(generics.ListCreateAPIView, IsOwnerOrReadOnly):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = CategoryBrand.objects.all()
    serializer_class = CategoryBrandSerializer


class ProductList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ShopProductList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ShopProduct.objects.all()
    serializer_class = ShopProductSerializer


class CommentsList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
