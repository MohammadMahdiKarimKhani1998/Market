from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    mobile = models.IntegerField(_('mobile'), null=True, blank=True)
    image = models.ImageField(_('Image'), upload_to='media/accounts/user', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Address(models.Model):
    city = models.TextField(_('City'), null=False, blank=False, max_length=150)
    street = models.TextField(_('Street'), null=False, blank=False, max_length=150)
    allay = models.TextField(_('Allay'), null=False, blank=False, max_length=150)
    zip_code = models.IntegerField(_('Zip code'), null=False, blank=False)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
        unique_together = [["user", "city", "street", "allay", "zip_code"]]

    def __str__(self):
        return self.user.email


class UserEmail(models.Model):
    email_to = models.EmailField(_('Email to'), null=False, blank=False)
    subject = models.CharField(_('Subject'), null=True, blank=True, max_length=150)
    body = models.TextField(_('Body'), null=True, blank=True)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Email")
        verbose_name_plural = _("Emails")
        unique_together = [["user", "email_to"]]

    def __str__(self):
        return self.subject


class Shop(models.Model):
    slug = models.SlugField(_('Slug'))
    name = models.CharField(_('Name'), null=False, blank=False, max_length=150)
    description = models.TextField(_('Description'), null=True, blank=True)
    image = models.ImageField(_('Image'), upload_to='media/accounts/shop/images', null=True, blank=True)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    publish_time = models.DateTimeField(_("Publish at"), db_index=True)

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")
        ordering = ['publish_time']

    def __str__(self):
        return self.slug


class Notification(models.Model):
    pass


class Likes(models.Model):
    pass


