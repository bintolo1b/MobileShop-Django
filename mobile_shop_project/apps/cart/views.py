from django.shortcuts import render
from apps.products.models import PhoneVariant
from apps.users.models import Client, CustomUser
from .models import Cart, Cart_PhoneVariant
from . import service
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required


# Create your views here.
def is_client(user):
    return user.is_authenticated and user.role == "client"

@user_passes_test(is_client)
def cart_view(request):
    try:
        # Lấy client từ user đã đăng nhập
        client = Client.objects.get(username=request.user)
        
        # Lấy hoặc tạo cart của client
        cart, created = Cart.objects.get_or_create(client=client)
        
        # Lấy danh sách sản phẩm trong giỏ hàng
        cart_items = Cart_PhoneVariant.objects.filter(cart=cart)

        cart_data = []
        total_price = 0
        for item in cart_items:
            item_data = {
                'color': item.phone_variant.color,
                'price': item.phone_variant.price,
                'stock': item.phone_variant.stock,
                'img': item.phone_variant.img,
                'ram': item.phone_variant.configuration.ram,
                'rom': item.phone_variant.configuration.rom,
                'name': item.phone_variant.phone.name,
                'quantity': item.quantity,
                'variant_id': item.phone_variant.id,
                'subtotal': item.phone_variant.price * item.quantity
            }
            cart_data.append(item_data)
            total_price += item_data['subtotal']

        context = {
            'cart_items': cart_data,
            'total_price': total_price
        }
        
        return render(request, 'cart/cart.html', context)

    except Client.DoesNotExist:
        return render(request, 'cart/cart.html', {'error': 'Không tìm thấy thông tin khách hàng'})
    except Exception as e:
        return render(request, 'cart/cart.html', {'error': str(e)})
