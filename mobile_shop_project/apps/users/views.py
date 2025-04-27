from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import Client
from apps.orders.models import Order, PhoneVariant_Order
from datetime import date
from django.utils.timezone import localtime
from datetime import datetime, timedelta
from django.db.models import Sum, Avg, Count, F
from apps.products.models import PhoneVariant
from django.utils import timezone
from datetime import datetime, timedelta
from mobile_shop_project.service import get_top_selling_phones

# Create your views here.
def is_staff(user):
    return user.is_authenticated and user.role == "staff"

@user_passes_test(is_staff)
def staff_home(request):
    # Lấy ngày hôm nay và hôm qua
    today = timezone.localtime(timezone.now()).date()
    yesterday = today - timedelta(days=1)
    
    # Đơn hàng hôm nay - sử dụng localtime để đảm bảo múi giờ chính xác
    start_of_day = timezone.make_aware(datetime.combine(today, datetime.min.time()), timezone.get_current_timezone())
    end_of_day = timezone.make_aware(datetime.combine(today, datetime.max.time()), timezone.get_current_timezone())
    today_orders = Order.objects.filter(time__range=(start_of_day, end_of_day))
    today_order_count = today_orders.count()
    
    # Đơn hàng hôm qua
    start_of_yesterday = timezone.make_aware(datetime.combine(yesterday, datetime.min.time()), timezone.get_current_timezone())
    end_of_yesterday = timezone.make_aware(datetime.combine(yesterday, datetime.max.time()), timezone.get_current_timezone())
    yesterday_orders = Order.objects.filter(time__range=(start_of_yesterday, end_of_yesterday))
    yesterday_order_count = yesterday_orders.count()
    
    # Tính phần trăm thay đổi số lượng đơn hàng
    order_percentage = 0
    if yesterday_order_count > 0:
        order_percentage = ((today_order_count - yesterday_order_count) / yesterday_order_count) * 100
    
    # Doanh thu hôm nay
    today_revenue = PhoneVariant_Order.objects.filter(order__time__range=(start_of_day, end_of_day)).aggregate(
        total=Sum(F('price') * F('quantity')))['total'] or 0
    
    # Doanh thu hôm qua
    yesterday_revenue = PhoneVariant_Order.objects.filter(order__time__range=(start_of_yesterday, end_of_yesterday)).aggregate(
        total=Sum(F('price') * F('quantity')))['total'] or 0
    
    # Tính phần trăm thay đổi doanh thu
    revenue_percentage = 0
    if yesterday_revenue > 0:
        revenue_percentage = ((today_revenue - yesterday_revenue) / yesterday_revenue) * 100
    
    # Giá trị đơn hàng trung bình hôm nay
    today_avg_order_value = 0
    if today_order_count > 0:
        today_avg_order_value = today_revenue / today_order_count
    
    # Giá trị đơn hàng trung bình hôm qua
    yesterday_avg_order_value = 0
    if yesterday_order_count > 0:
        yesterday_avg_order_value = yesterday_revenue / yesterday_order_count
    
    # Tính phần trăm thay đổi giá trị đơn hàng trung bình
    avg_order_percentage = 0
    if yesterday_avg_order_value > 0:
        avg_order_percentage = ((today_avg_order_value - yesterday_avg_order_value) / yesterday_avg_order_value) * 100
    
    # 3 đơn hàng gần đây nhất
    recent_orders = Order.objects.all().order_by('-time')[:3]
    recent_orders_data = []
    
    for order in recent_orders:
        order_items = PhoneVariant_Order.objects.filter(order=order)
        items_data = []
        total = 0
        
        for item in order_items:
            item_data = {
                'name': item.phonevariant.phone.name,
                'color': item.phonevariant.color,
                'ram': item.phonevariant.configuration.ram,
                'rom': item.phonevariant.configuration.rom,
                'quantity': item.quantity,
                'price': item.price,
                'subtotal': item.price * item.quantity
            }
            items_data.append(item_data)
            total += item.price * item.quantity
        
        order_data = {
            'id': order.id,
            'status': order.status,
            'date': order.time,
            'items': items_data,
            'total': total
        }
        recent_orders_data.append(order_data)
    
    # Sử dụng hàm get_top_selling_phones để lấy 3 điện thoại bán chạy nhất
    top_phones = get_top_selling_phones()[:3]
    top_phones_data = []
    
    for phone in top_phones:
        phone_data = {
            'name': phone.name,
            'price': phone.price,
            'sold_quantity': phone.sold_quantity,
            'img': phone.img
        }
        top_phones_data.append(phone_data)
    
    context = {
        'today_order_count': today_order_count,
        'order_percentage': round(order_percentage, 2),
        'today_revenue': today_revenue,
        'revenue_percentage': round(revenue_percentage, 2),
        'today_avg_order_value': round(today_avg_order_value, 2),
        'avg_order_percentage': round(avg_order_percentage, 2),
        'recent_orders': recent_orders_data,
        'top_phones': top_phones_data
    }
    
    return render(request, 'staff/staff_home.html', context)

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
                'date': localtime(order.time).strftime('%H:%M:%S %d/%m/%Y'),
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
    
@user_passes_test(is_staff)
def add_phone(request):
    return render(request, 'staff/staff_add_phone.html')

@user_passes_test(is_staff)
def add_phone_variant(request):
    return render(request, 'staff/staff_add_phonevariant.html')