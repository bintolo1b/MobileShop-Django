from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Client, CustomUser

@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"message": "Username and password are required"}, status=400)

    user = authenticate(username=username, password=password)

    if user:
        # xóa session cũ
        request.session.flush() 

        login(request, user)  # 👉 Lưu trạng thái đăng nhập vào session

        request.session['username'] = username
        request.session['role'] = user.role
        
        return Response({
            "message": "Login successful",
            "role": user.role  # 👉 Trả về role của user
        })
    
    return Response({"message": "Invalid credentials"}, status=401)

@api_view(["POST"])
def logup_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    confirm_password = request.data.get("confirm_password")
    firstname = request.data.get("firstname")
    lastname = request.data.get("lastname") 
    email = request.data.get("email")
    phone = request.data.get("phone")
    address = request.data.get("address")

    # Kiểm tra các trường bắt buộc
    if not all([username, password, confirm_password, firstname, lastname, email, phone, address]):
        return Response({"message": "Vui lòng điền đầy đủ thông tin"}, status=400)

    # Kiểm tra password và confirm_password có khớp không
    if password != confirm_password:
        return Response({"message": "Mật khẩu xác nhận không khớp"}, status=400)

    try:
        # Kiểm tra username đã tồn tại chưa
        if CustomUser.objects.filter(username=username).exists():
            return Response({"message": "Tên đăng nhập đã tồn tại"}, status=400)

        # Kiểm tra email đã tồn tại chưa
        if CustomUser.objects.filter(email=email).exists():
            return Response({"message": "Email đã tồn tại"}, status=400)

        # Kiểm tra lại password và confirm_password trước khi tạo user
        if password != confirm_password:
            return Response({"message": "Mật khẩu xác nhận không khớp"}, status=400)

        # Tạo user mới
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=firstname,
            last_name=lastname,
            phone=phone,
            address=address
        )

        # Tạo client profile
        client = Client.objects.create(
            username=user
        )

        return Response({"message": "Đăng ký thành công"}, status=201)

    except Exception as e:
        return Response({"message": f"Lỗi: {str(e)}"}, status=400)


@api_view(["POST"])
def logout_view(request):
    logout(request)  # 👉 Xóa session
    return Response({"message": "Logged out"})
