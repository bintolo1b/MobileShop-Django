from django.shortcuts import render

# Create your views here.
def phone_detail(request):
    return render(request, 'phone/detail.html')