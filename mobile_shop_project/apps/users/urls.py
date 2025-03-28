from django.urls import path
from . import api
from . import views

urlpatterns = [
    path('login/', api.login_view),
    path('logout/', api.logout_view),
    path('logup/', api.logup_view),
    path('staff/', views.staff_home)
]