from django.db import models
from django.utils.translation import ugettext_lazy as _


class Slide(models.Model):
    slug = models.SlugField(_('Slug'))
    image = models.ImageField(_('Image'), upload_to='media/home/images', null=True, blank=True)

    class Meta:
        verbose_name = _("Slide")
        verbose_name_plural = _("Slides")

