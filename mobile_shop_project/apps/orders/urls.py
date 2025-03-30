from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.order_view),
    path('order_infor/', views.order_infor_view),
    path('customer_infor/', views.customer_infor),
    path('confirm_payment/', api.confirm_payment_view),
    path('order_detail/<int:order_id>/', api.order_detail_view),
]