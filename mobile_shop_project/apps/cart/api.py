from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Cart, Cart_PhoneVariant
from apps.products.models import PhoneVariant
from apps.users.models import Client, CustomUser

@api_view(["POST"])
def addToCart_view(request):
    # Lấy phone_variant_id từ request
    phone_variant_id = request.data.get('phone_variant_id')
    quantity = request.data.get('quantity', 1)
    
    if not request.user.is_authenticated:
        return Response({"message": "Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng"}, status=401)
    
    try:
        # Lấy client từ user
        client = Client.objects.get(username=request.user)
        
        # Lấy cart của client
        cart, created = Cart.objects.get_or_create(client=client)
        
        # Lấy phone variant
        phone_variant = PhoneVariant.objects.get(id=phone_variant_id)
        
        # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
        cart_item, item_created = Cart_PhoneVariant.objects.get_or_create(
            cart=cart,
            phone_variant=phone_variant,
            defaults={'quantity': quantity}
        )
        
        # Nếu sản phẩm đã có trong giỏ hàng, tăng số lượng
        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return Response({"message": "Đã thêm sản phẩm vào giỏ hàng thành công"}, status=200)
    
    except PhoneVariant.DoesNotExist:
        return Response({"message": "Không tìm thấy sản phẩm"}, status=404)
    except Exception as e:
        return Response({"message": f"Lỗi: {str(e)}"}, status=400)
    