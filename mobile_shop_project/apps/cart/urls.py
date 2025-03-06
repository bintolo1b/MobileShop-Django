from django.urls import path
from . import views
from . import api
urlpatterns = [
    # path('phone/<int:phone_id>/', views.phone_detail),
    path('', views.cart_view),
    path('add-to-cart/', api.addToCart_view)
]