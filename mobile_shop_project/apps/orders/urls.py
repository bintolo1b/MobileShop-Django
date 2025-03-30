from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.order_view),
    path('order_infor/', views.order_infor_view),
    path('customer_infor/', views.customer_infor),
    path('confirm_payment/', api.confirm_payment_view),
]