from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.order_view),
    path('order_infor', views.order_infor_view)
]