from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('phone/<int:phone_id>/', views.phone_detail),
    path('phonebybrand/', views.phone_by_brand),
    path('api/phonevariant/', api.get_phone_variant),
    path('api/rating/', api.create_rating),
    path('api/rating/count/<int:product_id>/', api.get_product_ratings),
    path('api/rating/<int:product_id>/', api.get_product_rating_details),
    path('api/rating/client/<int:product_id>/', api.get_client_product_rating),
    path('api/search/', api.search_products_by_name),
    path('api/phone/', api.add_new_phone),
    path('api/phonevariant/add/', api.add_phone_variant),
]