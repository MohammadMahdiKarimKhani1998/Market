from django.db import models
from product.models import ShopProduct
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    description = models.TextField(_("Description"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    user = models.ForeignKey(User, verbose_name=_('User'), null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-updated_at']

    def __str__(self):
        return self.description


class OrderItem (models.Model):
    count = models.IntegerField(_("Count"))
    price = models.IntegerField(_("Price"))
    order = models.ForeignKey(Order, verbose_name=_("Order"), on_delete=models.CASCADE)
    shop_product = models.ForeignKey(ShopProduct, verbose_name=_("Shop_Product"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Order_Item")
        verbose_name_plural = _("Order_Items")
        ordering = ['-count']

    def __str__(self):
        return str(self.order) + str(self.shop_product)


class Basket (models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Basket")
        verbose_name_plural = _("Baskets")

    def __str__(self):
        return self.user.email


class BasketItems(models.Model):
    count = models.IntegerField(_("Count"))
    price = models.IntegerField(_("Price"))
    basket = models.ForeignKey(Basket, verbose_name=_('Basket'), on_delete=models.CASCADE)
    shop_product = models.ForeignKey(ShopProduct, verbose_name=_('Shop_Product'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Basket_Item")
        verbose_name_plural = _("Basket_Items")

    def __str__(self):
        return "basket:" + str(self.basket) + "shop_product:" + str(self.shop_product)


class Payment(models.Model):
    order = models.ForeignKey(Order, verbose_name=_("Order"), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    amount = models.IntegerField(_("Amount"))

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return "order:" + str(self.order) + "user:" + str(self.user)
