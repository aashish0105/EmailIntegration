from django.urls import path
from .views import *
urlpatterns=[
    path('home/',homeview,name='home'),
    path('aboutus/',aboutusview,name='aboutus'),
]