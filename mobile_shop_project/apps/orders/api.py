from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Client, Order, PhoneVariant, PhoneVariant_Order
from apps.cart.models import Cart, Cart_PhoneVariant
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required
import json

@api_view(["POST"])
def confirm_payment_view(request):
    if request.method == "POST":
        try:
            # Lấy username từ session
            username = request.user.username
            
            # Tìm Client theo username
            client = get_object_or_404(Client, username=username)
            
            # Lấy Cart của Client
            cart = get_object_or_404(Cart, client=client)
            
            # Lấy tất cả PhoneVariant trong Cart
            cart_items = Cart_PhoneVariant.objects.filter(cart=cart)
            
            if not cart_items.exists():
                return Response({"message": "Giỏ hàng trống"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Kiểm tra số lượng tồn kho của từng sản phẩm
            for cart_item in cart_items:
                if cart_item.phone_variant.stock < cart_item.quantity:
                    return Response({
                        "message": f"Sản phẩm {cart_item.phone_variant.phone.name} - {cart_item.phone_variant.color} - {cart_item.phone_variant.configuration} không đủ số lượng trong kho",
                        "available": cart_item.phone_variant.stock,
                        "requested": cart_item.quantity
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Lấy dữ liệu từ request để tạo Order
            data = json.loads(request.POST.get('data', '{}'))
            
            # Tạo Order mới
           
            order = Order.objects.create(
                payment_method=data.get('payment_method'),
                client_phone=data.get('client_phone'),
                client_name=data.get('client_name'),
                address=data.get('address'),
                email=data.get('email'),
                time=timezone.now(),
                client=client,
                status='Đang xử lý',
                payment_screenshot=request.FILES.get('payment_screenshot') if 'payment_screenshot' in request.FILES else None,
                note=data.get('note', '')
            )
            
            # Tạo PhoneVariant_Order cho từng item trong giỏ hàng
            for cart_item in cart_items:
                from .models import PhoneVariant_Order
                PhoneVariant_Order.objects.create(
                    phonevariant=cart_item.phone_variant,
                    order=order,
                    quantity=cart_item.quantity,
                    price=cart_item.phone_variant.price
                )
                
                # Cập nhật số lượng tồn kho và số lượng đã bán
                phone_variant = cart_item.phone_variant
                phone_variant.stock -= cart_item.quantity
                phone_variant.sold_quantity += cart_item.quantity
                phone_variant.save()
            
            # Xóa Cart sau khi đã tạo Order
            cart_items.delete()
            
            return Response({"message": "Đặt hàng thành công", "order_id": order.id}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"message": f"Lỗi: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(["GET"])
def order_detail_view(request, order_id):
    try:
        # Lấy thông tin đơn hàng
        order = get_object_or_404(Order, id=order_id)
        
        # Lấy các sản phẩm trong đơn hàng
        order_items = PhoneVariant_Order.objects.filter(order=order)
        
        items_data = []
        for item in order_items:
            item_data = {
                'name': item.phonevariant.phone.name,
                'color': item.phonevariant.color,
                'ram': item.phonevariant.configuration.ram,
                'rom': item.phonevariant.configuration.rom,
                'quantity': item.quantity,
                'price': item.price,
                'subtotal': item.price * item.quantity,
                'img': item.phonevariant.img.url if item.phonevariant.img else None
            }
            items_data.append(item_data)
        
        order_data = {
            'id': order.id,
            'status': order.status,
            'date': localtime(order.time).strftime('%H:%M:%S %d/%m/%Y'),
            'payment_method': order.payment_method,
            'payment_screenshot': order.payment_screenshot.url if order.payment_screenshot else None,
            'items': items_data,
            'total': sum(item['subtotal'] for item in items_data),
            'client': {
                'username': order.client.username.username,
                'fullname': order.client_name,
                'phone': order.client_phone,
                'email': order.email,
                'address': order.address
            },
            'note': order.note
        }
        
        return Response(order_data, status=status.HTTP_200_OK)
    
    except Order.DoesNotExist:
        return Response({"message": "Không tìm thấy đơn hàng"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": f"Lỗi: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    

@login_required
@api_view(["PUT"])
def update_order_status_view(request, order_id):
    try:
        # Lấy thông tin đơn hàng
        order = get_object_or_404(Order, id=order_id)
        
        # Kiểm tra quyền hạn
        user = request.user
        is_staff = user.is_authenticated and user.role == "staff"
        is_client = user.is_authenticated and user.role == "client"
        
        # Nếu là client, kiểm tra đơn hàng có thuộc về client đó không
        if is_client:
            try:
                client = Client.objects.get(username=user)
                if order.client.id != client.id:
                    return Response({"message": "Bạn không có quyền cập nhật đơn hàng này"}, status=status.HTTP_403_FORBIDDEN)
            except Client.DoesNotExist:
                return Response({"message": "Không tìm thấy thông tin khách hàng"}, status=status.HTTP_403_FORBIDDEN)
        
        # Nếu không phải staff hoặc client có đơn hàng đó thì không có quyền
        if not is_staff and not is_client:
            return Response({"message": "Bạn không có quyền cập nhật đơn hàng"}, status=status.HTTP_403_FORBIDDEN)
        
        # Kiểm tra dữ liệu đầu vào
        if 'status' not in request.data:
            return Response({"message": "Thiếu thông tin trạng thái đơn hàng"}, status=status.HTTP_400_BAD_REQUEST)
            
        new_status = request.data['status']
        
        # Các trạng thái hợp lệ cho đơn hàng
        valid_statuses = ['Đang xử lý', 'Đang vận chuyển', 'Đã giao hàng', 'Đã hủy']
        
        if new_status not in valid_statuses:
            return Response({
                "message": "Trạng thái không hợp lệ",
                "valid_statuses": valid_statuses
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Giới hạn quyền của client, client chỉ có thể đổi thành Đã giao hàng hoặc Đã hủy
        if is_client and new_status not in ['Đã giao hàng', 'Đã hủy']:
            return Response({"message": "Khách hàng chỉ có quyền đổi thành Đã giao hàng hoặc Đã hủy"}, status=status.HTTP_403_FORBIDDEN)
        
        # Client chỉ có thể đổi status thành Đã giao hàng khi trạng thái đơn hàng trước đó đang ở trạng thái Đang vận chuyển
        if is_client and new_status == 'Đã giao hàng' and order.status != 'Đang vận chuyển':
            return Response({"message": "Chỉ có thể đổi thành Đã giao hàng khi đơn hàng đang ở trạng thái Đang vận chuyển"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Giới hạn quyền của staff, staff chỉ có thể đổi thành Đang xử lý, Đang vận chuyển hoặc Đã hủy
        if is_staff and new_status not in ['Đang xử lý', 'Đang vận chuyển', 'Đã hủy']:
            return Response({"message": "Nhân viên chỉ có quyền đổi thành Đang xử lý, Đang vận chuyển hoặc Đã hủy"}, status=status.HTTP_403_FORBIDDEN)
        
        # Cập nhật trạng thái đơn hàng
        order.status = new_status
        order.save()
        
        return Response({
            "message": "Cập nhật trạng thái đơn hàng thành công",
            "order_id": order.id,
            "new_status": new_status
        }, status=status.HTTP_200_OK)
        
    except Order.DoesNotExist:
        return Response({"message": "Không tìm thấy đơn hàng"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": f"Lỗi: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    
