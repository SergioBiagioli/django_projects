from django.urls import path
from . import views

app_name = 'hello'
urlpatterns = [
    path("", views.hello_view, name="index"),
    ]

    #path('', TemplateView.as_view(template_name='home/main.html'))