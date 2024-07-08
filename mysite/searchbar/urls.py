from django.contrib import admin
from django.urls import path
from vehicles.views import MainView

urlpatterns = [
    path('', MainView.as_view(), name='mainsearch'),
]