from django.urls import path
from .views import *
urlpatterns=[
    path('login/',loginview,name='login'),
    path('logout/',logoutview,name='logout'),
    path('register/',registerview,name='register'),
]