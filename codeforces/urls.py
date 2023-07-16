from django.urls import path
from codeforces import views

urlpatterns = [
    path('add/profile/',views.AddProfile),
    path('verify/profile/',views.VerifyProfile),
]
