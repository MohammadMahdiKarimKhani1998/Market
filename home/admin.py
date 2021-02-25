from django.contrib import admin
from home.models import Slide


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('slug',)
    list_filter = ('slug', )
    search_fields = ('slug', )

