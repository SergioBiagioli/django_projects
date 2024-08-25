from django.urls import path, reverse_lazy
from . import views

app_name='newapp'
urlpatterns = [
    path('', views.ShowText.as_view(), name='main')
]