from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from . models import Client
from apps.cart.models import Cart, Cart_PhoneVariant

def is_client(user):
    return user.is_authenticated and user.role == "client"

@user_passes_test(is_client)
def order_view(request):
    return render(request, 'orders/orders.html')

@user_passes_test(is_client)
def order_infor_view(request):
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


        fullname = client.username.first_name +" "+client.username.last_name
        print(fullname)
        context = {
            'cart_items': cart_data,
            'total_price': total_price,
            'client_name': fullname,
            'phone_number': client.username.phone,
            'email': client.username.email,
            'address': client.username.address
        }
        
        return render(request, 'orders/order_infor.html', context)

    except Client.DoesNotExist:
        return render(request, 'orders/order_infor.html', {'error': 'Không tìm thấy thông tin khách hàng'})
    except Exception as e:
        return render(request, 'orders/order_infor.html', {'error': str(e)})
    
@user_passes_test(is_client)
def customer_infor(request):
    return render(request, 'orders/customer_infor.html')