from django.urls import path
from . import api

urlpatterns = [
    path('login/', api.login_view),
    path('logout/', api.logout_view),
]