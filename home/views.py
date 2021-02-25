import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic import ListView

from rest_framework import generics
from home.models import Slide
from home.serializers import SlideSerializer
from product.models import Category, Product
from rest_framework import permissions


class HomeView(ListView):
    model = Category
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ErrorView(TemplateView):
    template_name = "home/404.html"


@csrf_exempt
def search(request):
    data = json.loads(request.body)
    word = data['word']
    product_slugs = Product.objects.filter(slug__icontains=word)
    product_names = Product.objects.filter(name__icontains=word)

    search_list = []
    search_products_slugs = []
    search_products_shops = []

    for product in product_slugs:
        search_list.append(product.slug)
        search_products_slugs.append(product.slug)
        search_products_shops.append(product.property().shop.slug)
    for product in product_names:
        search_list.append(product.name)
        search_products_slugs.append(product.slug)
        search_products_shops.append(product.property().shop.slug)

    response = {"list": search_list, "slugs": search_products_slugs, "shops": search_products_shops}
    return HttpResponse(json.dumps(response), status=201)


# rest
class SlideList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer
