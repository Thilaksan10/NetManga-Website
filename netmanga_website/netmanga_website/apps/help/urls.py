from django.urls import path

from .views import help

app_name='help'
urlpatterns = [
    path('',help,name='help'),
]