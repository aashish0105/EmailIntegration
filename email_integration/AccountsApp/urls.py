from django.urls import path
from .views import *
urlpatterns=[
    path('login/',loginview,name='login'),
    path('logout/',logoutview,name='logout'),
    path('register/',registerview,name='register'),
    path('activate/<uidb64>/<token>',
        activate, name='activate'),
    path('success/',email_verification_success,name='success')
]