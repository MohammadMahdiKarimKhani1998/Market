from rest_framework import serializers

from home.models import Slide


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = ['slug', 'image']

