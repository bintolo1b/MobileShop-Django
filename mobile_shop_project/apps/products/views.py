from django.shortcuts import render, get_object_or_404
from .models import Phone, PhoneVariant, Product
from django.core.paginator import Paginator
from django.db.models import Min
from . import service


# Create your views here.
def phone_detail(request, phone_id):
    product = get_object_or_404(Product, id=phone_id)
    phone = get_object_or_404(Phone, id=phone_id)
    phone_variants = phone.phonevariant_set.all()  # Lấy danh sách biến thể của điện thoại

    # Lấy id nhỏ nhất của mỗi màu (để đại diện cho từng màu)
    color_variants = (
        phone.phonevariant_set
        .values('color')
        .annotate(min_id=Min('id')) #annotate này sẽ group by theo color rồi tìm min id đặt tên là min_id
    )

    configuration_variants = (
        phone.phonevariant_set
        .values('configuration_id')
        .annotate(min_id=Min('id'))
    )

    # Lấy danh sách PhoneVariant tương ứng với id đã lọc
    phone_variants_distinct_color = PhoneVariant.objects.filter(id__in=[v['min_id'] for v in color_variants])
    phone_variants_distinct_configuration = PhoneVariant.objects.filter(id__in=[v['min_id'] for v in configuration_variants])


    return render(request, 'phone/detail.html', {
        'product': product,
        'phone': phone,
        'phone_variants': phone_variants,  # Truyền biến, không phải chuỗi
        'phone_variants_distinct_color': phone_variants_distinct_color,
        'phone_variants_distinct_configuration': phone_variants_distinct_configuration
    })


def phone_by_brand(request):
    brand = request.GET.get('brand', '')  # Lấy brand từ request, mặc định là chuỗi rỗng
    page = int(request.GET.get('page', 1))  # Lấy page, mặc định là 1

    phones = service.get_phones_by_brand(brand, page)
    totalPages = service.get_total_pages_of_phone_by_brand(brand)

    page_numbers = list(range(1, totalPages + 1))
    return render(request, 'phone/category.html', {'phones': phones, 'brand': brand, 'page_numbers': page_numbers, 'current_page': page})