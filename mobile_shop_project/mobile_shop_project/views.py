from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import service

def homepage(request):
    top_phones = service.get_top_selling_phones()
    top_Xiaomi_phones = service.get_top_selling_phones_by_brand('Xiaomi')
    top_iPhone_phones = service.get_top_selling_phones_by_brand('iPhone')
    top_Realme_phones = service.get_top_selling_phones_by_brand('Realme')
    print(top_phones)
    return render(request, 'home.html', 
                  {'top_phones': top_phones, 
                   'top_Xiaomi_phones': top_Xiaomi_phones,
                   'top_iPhone_phones': top_iPhone_phones,
                   'top_Realme_phones': top_Realme_phones
                   })

def login(request):
    return render(request, 'login.html')

# @login_required
def signup(request):
    return render(request, 'signup.html')