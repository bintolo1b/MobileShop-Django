from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery, Sum
from django.db.models.functions import Coalesce
from .models import Product, PhoneVariant
import math

def get_phones_by_brand(brand, page_index, per_page=15):
    """
    Lấy danh sách sản phẩm theo thương hiệu, kèm theo biến thể đại diện, ảnh và giá.
    """
    products_qs = Product.objects.all()
    if brand:
        products_qs = products_qs.filter(phone__brand=brand)  # Lọc theo brand của phone

    # Truy vấn biến thể đại diện (biến thể có ID nhỏ nhất)
    min_variant_subquery = PhoneVariant.objects.filter(
        phone=OuterRef("pk")  # Cần tham chiếu đến phone từ product
    ).order_by("id").values("id")[:1]

    # Calculate total sold quantity for each phone
    sold_quantity_subquery = PhoneVariant.objects.filter(
        phone=OuterRef("pk")
    ).values("phone").annotate(
        total_sold=Sum("sold_quantity")
    ).values("total_sold")

    # Lấy ảnh và giá của biến thể đại diện
    products_qs = products_qs.annotate(
        variant_id=Subquery(min_variant_subquery),
        img=Subquery(PhoneVariant.objects.filter(id=OuterRef("variant_id")).values("img")[:1]),
        price=Subquery(PhoneVariant.objects.filter(id=OuterRef("variant_id")).values("price")[:1]),
        sold_quantity=Coalesce(Subquery(sold_quantity_subquery), 0)
    )

    # Phân trang
    paginator = Paginator(products_qs, per_page)
    return paginator.get_page(page_index)

def get_total_pages_of_phone_by_brand(brand):
    products_qs = Product.objects.all()
    if brand:
        products_qs = products_qs.filter(phone__brand=brand)
    total_products = products_qs.count()
    total_pages = math.ceil(total_products / 15)

    return total_pages
