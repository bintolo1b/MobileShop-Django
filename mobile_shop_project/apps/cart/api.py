from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Cart, Cart_PhoneVariant
from apps.products.models import PhoneVariant
from apps.users.models import Client, CustomUser
from django.contrib.auth.decorators import user_passes_test

@api_view(["POST"])
def addToCart_view(request):
    try:
        phone_variant_id = request.data.get('phone_variant_id')
        
        if not phone_variant_id:
            return Response({"message": "Thiếu phone_variant_id"}, status=400)

        quantity = int(request.data.get('quantity', 1))
        if quantity <= 0:
            return Response({"message": "Số lượng phải lớn hơn 0"}, status=400)

        if not request.user.is_authenticated:
            return Response({"message": "Vui lòng đăng nhập"}, status=401)

        client = Client.objects.filter(username=request.user).first()
        if not client:
            return Response({"message": "Chỉ client mới có thể thêm sản phẩm vào giỏ hàng"}, status=403)

        cart, _ = Cart.objects.get_or_create(client=client)
        phone_variant = PhoneVariant.objects.get(id=phone_variant_id)

        cart_item, item_created = Cart_PhoneVariant.objects.get_or_create(
            cart=cart,
            phone_variant=phone_variant,
            defaults={'quantity': quantity}
        )

        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({"message": "Đã thêm sản phẩm vào giỏ hàng thành công"}, status=200)

    except PhoneVariant.DoesNotExist:
        return Response({"message": "Không tìm thấy sản phẩm"}, status=404)
    
    except Exception as e:
        return Response({"message": f"Lỗi không xác định: {str(e)}"}, status=400)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cart, Cart_PhoneVariant
from apps.users.models import Client

@api_view(['PUT'])
def update_quantity(request, variant_id):
    try:
        if not request.user.is_authenticated:
            return Response({"message": "Vui lòng đăng nhập"}, status=401)
            
        quantity = int(request.GET.get('quantity', 1))
        client = Client.objects.get(username=request.user)
        cart = Cart.objects.get(client=client)
        cart_item = Cart_PhoneVariant.objects.get(cart=cart, phone_variant_id=variant_id)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        total_price = sum(item.phone_variant.price * item.quantity 
                         for item in Cart_PhoneVariant.objects.filter(cart=cart))
        
        return Response({
            "message": "Cập nhật số lượng thành công",
            "total_price": total_price
        }, status=200)
        
    except Exception as e:
        return Response({"message": str(e)}, status=400)


@api_view(["DELETE"])
def removeFromCart_view(request, variant_id):
    if not request.user.is_authenticated:
        return Response({"message": "Vui lòng đăng nhập"}, status=401)
    
    try:
        client = Client.objects.get(username=request.user)
        cart = Cart.objects.get(client=client)
        cart_item = Cart_PhoneVariant.objects.get(cart=cart, phone_variant_id=variant_id)
        cart_item.delete()
        return Response({"message": "Đã xóa sản phẩm khỏi giỏ hàng"}, status=200)
    except (Client.DoesNotExist, Cart.DoesNotExist, Cart_PhoneVariant.DoesNotExist):
        return Response({"message": "Không tìm thấy sản phẩm trong giỏ hàng"}, status=404)