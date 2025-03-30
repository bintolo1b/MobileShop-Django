from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Client, Order, PhoneVariant
from apps.cart.models import Cart, Cart_PhoneVariant
from django.utils import timezone
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
