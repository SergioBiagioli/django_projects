from django.contrib import admin
from django.urls import path
from vehicles.views import AplicationList

urlpatterns = [
    path('', AplicationList.as_view(), name='mainsearch'),
]