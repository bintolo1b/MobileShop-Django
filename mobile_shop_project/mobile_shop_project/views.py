from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import service
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response

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

@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    print(username, password)

    if not username or not password:
        return Response({"message": "Username and password are required"}, status=400)

    user = authenticate(username=username, password=password)
    print(user)

    if user:
        login(request, user)  # 👉 Lưu trạng thái đăng nhập vào session
        return Response({"message": "Login successful"})
    
    return Response({"message": "Invalid credentials"}, status=401)

@api_view(["GET"])
def check_login_status(request):
    if request.user.is_authenticated:
        return Response({"message": "Logged in", "user": request.user.username})
    return Response({"message": "Not logged in"}, status=401)

@api_view(["POST"])
def logout_view(request):
    logout(request)  # 👉 Xóa session
    return Response({"message": "Logged out"})