from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='bnss_to_crpc'),
]
