from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import Client
from apps.orders.models import Order, PhoneVariant_Order
# Create your views here.
def is_staff(user):
    return user.is_authenticated and user.role == "staff"

@user_passes_test(is_staff)
def staff_home(request):
    return render(request, 'staff/staff_home.html')

@user_passes_test(is_staff)
def staff_order(request):
    try: 
        # Lấy tất cả đơn hàng trong hệ thống
        orders = Order.objects.all().order_by('-id')
        
        orders_data = []
        for order in orders:
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
                    'img': item.phonevariant.img
                }
                items_data.append(item_data)
            
            
            order_data = {
                'id': order.id,
                'status': order.status,
                'date': order.time,
                'payment_method': order.payment_method,
                'payment_screenshot': order.payment_screenshot,
                'items': items_data,
                'total': sum(item['subtotal'] for item in items_data),
                'client': {
                    'username': order.client.username,
                    'fullname': order.client_name,
                    'phone': order.client_phone,
                    'email': order.email,
                    'address': order.address
                },
                'note': order.note
            }
            
            orders_data.append(order_data)
        
        context = {
            'orders': orders_data
        }
        
        return render(request, 'staff/staff_order.html', context)
    
    except Exception as e:
        return render(request, 'staff/staff_order.html', {'error': str(e)})