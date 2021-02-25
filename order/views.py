import json

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from rest_framework import generics, permissions

from account.models import Address
from order.forms import AddressForm
from order.models import BasketItems, Basket
from order.permissions import IsOwnerOrReadOnly
from order.serializers import BasketItemsSerializer
from product.models import ShopProduct, Category

User = get_user_model()


class BasketView(ListView, FormMixin):
    model = BasketItems
    template_name = 'order/shop.html'
    form_class = AddressForm

    def get_queryset(self):
        return BasketItems.objects.filter(basket__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(BasketView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['category_list'] = Category.objects.all()
        context['address'] = Address.objects.all()

        return context


def add_address(request):

    basketitems_list = BasketItems.objects.filter(basket__user=request.user)
    category_list = Category.objects.all()
    addresses = Address.objects.all()

    if request.method == 'POST':
        form = AddressForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print("yes")
            city = form.cleaned_data['city']
            street = form.cleaned_data['street']
            allay = form.cleaned_data['allay']
            code = form.cleaned_data['zip_code']
            address = Address.objects.create(city=city, street=street, allay=allay, zip_code=code, user=request.user)
            address.save()
        else:
            pass

        context = {
            'form': form,
            'basketitems_list': basketitems_list,
            'category_list': category_list,
            'address': addresses,
            'user': request.user
        }
    else:
        context = {
            'form': AddressForm(),
            'basketitems_list': basketitems_list,
            'category_list': category_list,
            'address': addresses,
            'user': request.user
        }
    return render(request, 'order/shop.html', context)


@csrf_exempt
def add_product_to_basket(request):
    data = json.loads(request.body)

    if request.user.is_authenticated:
        shop_product = ShopProduct.objects.get(id=data['shop_product_id'])

        if BasketItems.objects.filter(shop_product=shop_product):
            alert = "این محصول قبلا به سبد خرید شما اضافه شده است!"
            response = {'alert': alert}
            return HttpResponse(json.dumps(response), status=201)

        else:
            if Basket.objects.filter(user=request.user):
                BasketItems.objects.create(basket=Basket.objects.get(user=request.user), count=1,
                                           price=shop_product.price,
                                           shop_product=shop_product)
                alert = "محصول به سبد خرید شما اضافه شد."
                response = {'alert': alert}
                return HttpResponse(json.dumps(response), status=201)
            else:
                Basket.objects.create(user=request.user)
                BasketItems.objects.create(basket=Basket.objects.get(user=request.user), count=1,
                                           price=shop_product.price,
                                           shop_product=shop_product)
                alert = "محصول به سبد خرید شما اضافه شد."
                response = {'alert': alert}
                return HttpResponse(json.dumps(response), status=201)
    else:
        alert = "لطفا ابتدا به پروفایل خود وارد شوید!"
        response = {'alert': alert}
        return HttpResponse(json.dumps(response), status=201)


@csrf_exempt
def edit_table(request):
    data = json.loads(request.body)

    BasketItems.objects.filter(id=data['basket_item_id']).delete()

    response = {'r': "yes"}
    return HttpResponse(json.dumps(response), status=201)


# rest
class BasketItemsList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = BasketItems.objects.all()
    serializer_class = BasketItemsSerializer
