from django.urls import path
from . import api
from . import views

urlpatterns = [
    path('login/', api.login_view),
    path('logout/', api.logout_view),
    path('logup/', api.logup_view),
    path('api/clients/', api.get_all_clients),
    path('api/revenue/monthly/', api.get_monthly_revenue),
    path('api/change-password/', api.change_password),
    path('api/update-profile/', api.update_client_info),
    path('api/change-client-password/', api.change_client_password),
    path('staff/', views.staff_home, name='staff_home'),
    path('staff/orders/', views.staff_order, name='staff_order'),
    path('staff/add_phone/', views.add_phone, name='add_phone'),
    path('staff/add_phonevariant/', views.add_phone_variant, name='add_phone_variant'),
    path('staff/revenue/', views.staff_revenue, name='staff_revenue'),
    path('staff/clients/', views.staff_client, name='staff_client')
]