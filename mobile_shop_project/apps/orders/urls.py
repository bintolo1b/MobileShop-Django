from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.order_view),
]