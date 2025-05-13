from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Client, CustomUser
from django.utils import timezone
from django.utils.timezone import localtime
from apps.orders.models import Order, PhoneVariant_Order
from django.db.models import Sum, F
from datetime import datetime
import calendar

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

@api_view(["GET"])
def get_all_clients(request):
    """
    API trả về thông tin tất cả khách hàng
    """
    # Kiểm tra xem người dùng đã đăng nhập chưa
    if not request.user.is_authenticated:
        return Response({"message": "Bạn cần đăng nhập để thực hiện chức năng này"}, status=401)
    
    # Kiểm tra quyền hạn (chỉ admin và staff mới có quyền xem)
    if request.user.role not in ['admin', 'staff']:
        return Response({"message": "Bạn không có quyền thực hiện chức năng này"}, status=403)
    
    try:
        # Lấy danh sách tất cả client
        clients = Client.objects.all()
        
        # Tạo danh sách chứa thông tin chi tiết của từng client
        clients_data = []
        for client in clients:
            user = client.username
            clients_data.append({
                "id": client.id,
                "username": user.username,
                "email": user.email,
                "full_name": f"{user.first_name} {user.last_name}",
                "phone": user.phone,
                "address": user.address,
                "date_joined": localtime(user.date_joined).strftime('%H:%M:%S %d/%m/%Y')
            })
        
        return Response({
            "count": len(clients_data),
            "clients": clients_data
        }, status=200)
        
    except Exception as e:
        return Response({"message": f"Lỗi: {str(e)}"}, status=500)

@api_view(["POST"])
def get_monthly_revenue(request):
    """
    API trả về doanh thu theo tháng trong khoảng thời gian chỉ định
    Nhận vào 3 tham số: năm, tháng bắt đầu, tháng kết thúc
    """
    # Kiểm tra xem người dùng đã đăng nhập chưa
    if not request.user.is_authenticated:
        return Response({"message": "Bạn cần đăng nhập để thực hiện chức năng này"}, status=401)
    
    # Kiểm tra quyền hạn (chỉ admin và staff mới có quyền xem)
    if request.user.role not in ['admin', 'staff']:
        return Response({"message": "Bạn không có quyền thực hiện chức năng này"}, status=403)
    
    try:
        # Lấy các tham số từ request
        year = request.data.get('year')
        start_month = request.data.get('start_month')
        end_month = request.data.get('end_month')
        
        # Kiểm tra các tham số bắt buộc
        if not all([year, start_month, end_month]):
            return Response({
                "message": "Thiếu thông tin bắt buộc (year, start_month, end_month)"
            }, status=400)
            
        # Chuyển đổi tham số về dạng số nguyên
        try:
            year = int(year)
            start_month = int(start_month)
            end_month = int(end_month)
        except ValueError:
            return Response({
                "message": "Các thông số phải là số nguyên"
            }, status=400)
            
        # Kiểm tra giá trị của tháng
        if not (1 <= start_month <= 12 and 1 <= end_month <= 12):
            return Response({
                "message": "Tháng phải nằm trong khoảng từ 1 đến 12"
            }, status=400)
            
        # Đảm bảo tháng bắt đầu không lớn hơn tháng kết thúc
        if start_month > end_month:
            return Response({
                "message": "Tháng bắt đầu không được lớn hơn tháng kết thúc"
            }, status=400)
            
        # Khởi tạo danh sách kết quả
        monthly_revenue = []
        
        # Tính doanh thu từng tháng
        for month in range(start_month, end_month + 1):
            # Lấy số ngày trong tháng
            last_day = calendar.monthrange(year, month)[1]
            
            # Tạo datetime cho ngày đầu tiên và ngày cuối cùng của tháng
            start_date = timezone.make_aware(datetime(year, month, 1, 0, 0, 0))
            end_date = timezone.make_aware(datetime(year, month, last_day, 23, 59, 59))
            
            # Tính tổng doanh thu trong tháng, loại trừ đơn hàng đã hủy
            month_revenue = PhoneVariant_Order.objects.filter(
                order__time__range=(start_date, end_date)
            ).exclude(
                order__status="Đã hủy"  # Loại trừ đơn hàng đã hủy
            ).aggregate(
                total=Sum(F('price') * F('quantity'))
            )['total'] or 0
            
            # Thêm vào danh sách kết quả
            monthly_revenue.append({
                "month": month,
                "revenue": month_revenue
            })
        
        return Response({
            "year": year,
            "monthly_revenue": monthly_revenue
        }, status=200)
        
    except Exception as e:
        return Response({"message": f"Lỗi: {str(e)}"}, status=500)

@api_view(["POST"])
def change_password(request):
    """
    API đổi mật khẩu cho người dùng
    """
    # Kiểm tra xem người dùng đã đăng nhập chưa
    if not request.user.is_authenticated:
        return Response({"message": "Bạn cần đăng nhập để thực hiện chức năng này"}, status=401)
    
    try:
        # Lấy các tham số từ request
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        
        # Kiểm tra các tham số bắt buộc
        if not all([current_password, new_password, confirm_password]):
            return Response({
                "message": "Thiếu thông tin bắt buộc (current_password, new_password, confirm_password)"
            }, status=400)
        
        # Kiểm tra mật khẩu hiện tại có đúng không
        user = authenticate(username=request.user.username, password=current_password)
        if not user:
            return Response({
                "message": "Mật khẩu hiện tại không đúng"
            }, status=400)
        
        # Kiểm tra mật khẩu mới và xác nhận mật khẩu có khớp nhau không
        if new_password != confirm_password:
            return Response({
                "message": "Mật khẩu mới và xác nhận mật khẩu không khớp"
            }, status=400)
        
        # Kiểm tra mật khẩu mới có giống mật khẩu cũ không
        if current_password == new_password:
            return Response({
                "message": "Mật khẩu mới không được giống mật khẩu cũ"
            }, status=400)
        
        # Kiểm tra độ dài mật khẩu mới (ít nhất 8 ký tự)
        if len(new_password) < 8:
            return Response({
                "message": "Mật khẩu mới phải có ít nhất 8 ký tự"
            }, status=400)
        
        # Đổi mật khẩu
        user.set_password(new_password)
        user.save()
        
        # Cập nhật session để người dùng không bị đăng xuất
        login(request, user)
        
        return Response({
            "message": "Đổi mật khẩu thành công"
        }, status=200)
        
    except Exception as e:
        return Response({
            "message": f"Lỗi khi đổi mật khẩu: {str(e)}"
        }, status=500)

@api_view(["POST"])
def update_client_info(request):
    """
    API cho phép client cập nhật thông tin cá nhân: họ tên, số điện thoại, email, địa chỉ
    """
    # Kiểm tra xem người dùng đã đăng nhập chưa
    if not request.user.is_authenticated:
        return Response({"message": "Bạn cần đăng nhập để thực hiện chức năng này"}, status=401)
    
    # Kiểm tra quyền hạn (chỉ client mới có quyền cập nhật thông tin của mình)
    if request.user.role != 'client':
        return Response({"message": "Chức năng này chỉ dành cho khách hàng"}, status=403)
    
    try:
        # Lấy các tham số từ request
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        phone = request.data.get('phone')
        email = request.data.get('email')
        address = request.data.get('address')
        
        # Kiểm tra các tham số bắt buộc
        if not all([first_name, last_name, phone, email, address]):
            return Response({
                "message": "Thiếu thông tin bắt buộc (first_name, last_name, phone, email, address)"
            }, status=400)
        
        # Kiểm tra email đã tồn tại chưa (nếu email thay đổi)
        if email != request.user.email and CustomUser.objects.filter(email=email).exists():
            return Response({"message": "Email đã được sử dụng bởi tài khoản khác"}, status=400)
        
        # Cập nhật thông tin người dùng
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.email = email
        user.address = address
        user.save()
        
        return Response({
            "message": "Cập nhật thông tin thành công",
            "user_info": {
                "username": user.username,
                "full_name": f"{user.first_name} {user.last_name}",
                "phone": user.phone,
                "email": user.email,
                "address": user.address
            }
        }, status=200)
        
    except Exception as e:
        return Response({
            "message": f"Lỗi khi cập nhật thông tin: {str(e)}"
        }, status=500)

