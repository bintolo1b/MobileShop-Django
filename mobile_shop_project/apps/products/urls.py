from django.urls import path
from . import views

urlpatterns = [
    path('phonedetail/', views.phone_detail),
]