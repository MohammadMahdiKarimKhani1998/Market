from django.db import models
from account.models import Shop
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import Max, Min

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    slug = models.SlugField(_('Slug'))
    title = models.CharField(_('Title'), max_length=150)
    image = models.ImageField(_('Image'), upload_to='media/products/categories/images', null=True, blank=True)
    detail = models.TextField(_('Detail'), null=True, blank=True)
    parent = models.ForeignKey('self', verbose_name=_("Parent"), on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title

    def category_brand(self):
        return CategoryBrand.objects.filter(category=self)

    def product(self):
        return Product.objects.filter(category=self)

    def max_price(self):
        maximum = ShopProduct.objects.filter(product__category=self).aggregate(Max('price'))
        return int(maximum['price__max'])

    def min_price(self):
        minimum = ShopProduct.objects.filter(product__category=self).aggregate(Min('price'))
        return int(minimum['price__min'])

    def step(self):
        return (self.max_price()-self.min_price())/10


class Brand(models.Model):
    slug = models.SlugField(_('Slug'))
    name = models.CharField(_('Name'), max_length=150)
    image = models.ImageField(_('Image'), upload_to='media/products/brands/images', null=True, blank=True)
    detail = models.TextField(_('Detail'))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    publish_time = models.DateTimeField(_("Publish at"), db_index=True)

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")
        ordering = ['-created_at']

    def __str__(self):
        return self.slug


class CategoryBrand(models.Model):
    category = models.ForeignKey(Category, verbose_name=_('Category'), on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, verbose_name=_('Brand'), on_delete=models.CASCADE)

    class Meta:
        unique_together = ['category', 'brand']


class Product(models.Model):
    slug = models.SlugField(_('Slug'))
    name = models.CharField(_('Name'), db_index=True, max_length=150)
    image = models.ImageField(_('Image'), upload_to='media/products/images')
    detail = models.TextField(_('Detail'))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    publish_time = models.DateTimeField(_("Publish at"), db_index=True)
    brand = models.ForeignKey(Brand, verbose_name=_('Brand'), null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, verbose_name=_('Category'), null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['-updated_at']

    def __str__(self):
        return self.slug

    def property(self):
        return ShopProduct.objects.filter(product=self).first()

    def shop_product(self, slug):
        shop_products = ShopProduct.objects.filter(product=self)
        for shop_product in shop_products:
            if shop_product.shop.slug == slug:
                return shop_product


class ShopProduct(models.Model):
    price = models.IntegerField(_('Price'))
    quantity = models.IntegerField(_('Quantity'))
    shop = models.ForeignKey(Shop, verbose_name=_('Shop'), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_('Product'), on_delete=models.CASCADE)

    class Unit(models.TextChoices):
        toman = 'تومان', _('Toman')
        rial = 'ریال', _('Rial')

    unit = models.CharField(max_length=5, choices=Unit.choices, default=Unit.toman)

    class Meta:
        verbose_name = _("Shop Product")
        verbose_name_plural = _("Shop Products")
        unique_together = ['product', 'shop']

    def __str__(self):
        return "shop:"+str(self.shop)+",product:"+str(self.product)


class Comments(models.Model):
    content = models.TextField(_('Content'))
    rate = models.IntegerField(_('Rate'), null=True, blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    publish_time = models.DateTimeField(_("Publish at"), db_index=True, auto_now=True)
    product = models.ForeignKey(Product, verbose_name=_('Product'), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['publish_time']

    def __str__(self):
        return "user:"+str(self.user)+",product"+str(self.product)

    @property
    def like_count(self):
        q = CommentLike.objects.filter(comment=self, status=True)
        return q.count()

    @property
    def dislike_count(self):
        q = self.comment_like.filter(status=False)
        return q.count()

    @property
    def comment_likes(self):
        comment_like = CommentLike.objects.filter(comment=self)
        users = [i.user for i in comment_like]
        return {'comment_like': comment_like, 'users': users}


class CommentLike(models.Model):
    status = models.BooleanField(_("Status"), null=True, blank=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, verbose_name=_("Comment"), related_name="comment_like",
                                on_delete=models.CASCADE)

    class Meta:
        unique_together = [["user", "comment"]]
        verbose_name = _("Comment_Like")
        verbose_name_plural = _("Comment_Likes")

    def __str__(self):
        return str(self.status)


class Images(models.Model):
    image = models.ImageField(_('Image'), upload_to='media/products/images')
    product = models.ForeignKey(Product, verbose_name=_('Product'), on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    publish_time = models.DateTimeField(_("Publish at"), db_index=True)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        ordering = ['-created_at']

    def __str__(self):
        return self.product
