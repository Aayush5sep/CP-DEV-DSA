from django.urls import path
from . import views

urlpatterns = [
    path('add/profile/',views.AddProfile),
    path('verify/profile/',views.VerifyProfile),
]