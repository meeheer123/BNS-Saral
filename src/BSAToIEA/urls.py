from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='bsa_to_iea'),
]
