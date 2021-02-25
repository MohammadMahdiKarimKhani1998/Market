from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import HomeView, search, ErrorView, SlideList

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', search, name='search'),
    path('404/', ErrorView.as_view(), name="404"),
    path('api/slides/', SlideList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
