from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('phone/<int:phone_id>/', views.phone_detail),
    path('api/phonevariant/', api.get_phone_variant)
]