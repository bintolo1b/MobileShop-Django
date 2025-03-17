from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required



@login_required
def order_view(request):
    return render(request, 'orders/orders.html')