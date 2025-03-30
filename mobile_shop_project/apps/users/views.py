from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
def is_staff(user):
    return user.is_authenticated and user.role == "staff"

@user_passes_test(is_staff)
def staff_home(request):
    return render(request, 'staff/staff_home.html')

@user_passes_test(is_staff)
def staff_order(request):
    return render(request, 'staff/staff_order.html')