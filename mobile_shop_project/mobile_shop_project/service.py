from apps.products.models import Phone, PhoneVariant, Product
from django.db.models import Case, When, IntegerField, Sum, Value, Subquery, OuterRef, QuerySet

from apps.products.models import Rating
from django.db.models import Avg
import math

def get_average_rating(product_id):
    """
    Tính số sao trung bình của một sản phẩm và làm tròn đến 0.5
    
    Args:
        product_id: ID của sản phẩm cần tính rating
        
    Returns:
        float: Số sao trung bình đã làm tròn đến 0.5 (0.5, 1, 1.5, 2, 2.5,...)
    """
    # Lấy giá trị trung bình từ database
    avg_rating = Rating.objects.filter(product_id=product_id).aggregate(avg=Avg('star'))['avg']
    
    # Nếu không có rating nào, trả về 0
    if avg_rating is None:
        return 0
    
    # Làm tròn đến 0.5 gần nhất
    return round(avg_rating * 2) / 2


def get_top_selling_phones():
    top_phones_qs = (
        PhoneVariant.objects
        .values("phone")
        .annotate(sold_quantity=Sum("sold_quantity"))
        .order_by("-sold_quantity")
    )

    top_phone_ids = list(top_phones_qs.values_list("phone", flat=True)[:15])

    min_variant = PhoneVariant.objects.filter(
        phone=OuterRef("pk")
    ).order_by("id").values("id")[:1]

    sold_quantity_subquery = Subquery(
        top_phones_qs.filter(phone=OuterRef("pk")).values("sold_quantity")
    )

    # Tạo danh sách When để giữ đúng thứ tự
    order_case = Case(
        *[When(id=phone_id, then=Value(index)) for index, phone_id in enumerate(top_phone_ids)],
        output_field=IntegerField()
    )

    products = Product.objects.filter(id__in=top_phone_ids).annotate(
        variant_id=Subquery(min_variant),
        img=Subquery(PhoneVariant.objects.filter(id=OuterRef("variant_id")).values("img")[:1]),
        price=Subquery(PhoneVariant.objects.filter(id=OuterRef("variant_id")).values("price")[:1]),
        sold_quantity=sold_quantity_subquery,
        order_index=order_case  # Thêm trường này để sắp xếp
    ).order_by("order_index")  # Sắp xếp theo thứ tự mong muốn
    
    # Thêm average_rating cho từng sản phẩm
    for product in products:
        product.average_rating = get_average_rating(product.id)
    
    return products

def get_top_selling_phones_by_brand(brand):
    top_phones_qs = (
        PhoneVariant.objects
        .filter(phone__brand=brand)
        .values("phone")
        .annotate(sold_quantity=Sum("sold_quantity"))
        .order_by("-sold_quantity")
    )

    top_phone_ids = list(top_phones_qs.values_list("phone", flat=True)[:15])

    min_variant = PhoneVariant.objects.filter(
        phone=OuterRef("pk")
    ).order_by("id").values("id")[:1]

    sold_quantity_subquery = Subquery(
        top_phones_qs.filter(phone=OuterRef("pk")).values("sold_quantity")
    )

    # Tạo danh sách When để giữ đúng thứ tự
    order_case = Case(
        *[When(id=phone_id, then=Value(index)) for index, phone_id in enumerate(top_phone_ids)],
        output_field=IntegerField()
    )

    return Product.objects.filter(id__in=top_phone_ids).annotate(
        variant_id=Subquery(min_variant),
        img=Subquery(PhoneVariant.objects.filter(id=OuterRef("variant_id")).values("img")[:1]),
        price=Subquery(PhoneVariant.objects.filter(id=OuterRef("variant_id")).values("price")[:1]),
        sold_quantity=sold_quantity_subquery,
        order_index=order_case  # Thêm trường này để sắp xếp
    ).order_by("order_index")  # Sắp xếp theo thứ tự mong muốn


# def get_xiaomi_top_selling_phones():
#     top_phones_qs = (
#         PhoneVariant.objects
#         .filter(phone__brand='Xiaomi')
#         .values("phone")
#         .annotate(sold_quantity=Sum("sold_quantity"))
#         .order_by("-sold_quantity")
#     )

#     top_phone_ids = list(top_phones_qs.values_list("phone", flat=True)[:15])

#     min_variant = PhoneVariant.objects.filter(
#         phone=OuterRef("pk")
#     ).order_by("id").values("id")[:1]

#     sold_quantity_subquery = Subquery(
#         top_phones_qs.filter(phone=OuterRef("pk")).values("sold_quantity")
#     )

#     # Tạo danh sách When để giữ đúng thứ tự
#     order_case = Case(
#         *[When(id=phone_id, then=Value(index)) for index, phone_id in enumerate(top_phone_ids)],
#         output_field=IntegerField()
#     )

#     return Product.objects.filter(id__in=top_phone_ids).annotate(
#         variant_id=Subquery(min_variant),
#         img=Subquery(PhoneVariant.objects.filter(id=OuterRef("variant_id")).values("img")[:1]),
#         price=Subquery(PhoneVariant.objects.filter(id=OuterRef("variant_id")).values("price")[:1]),
#         sold_quantity=sold_quantity_subquery,
#         order_index=order_case  # Thêm trường này để sắp xếp
#     ).order_by("order_index")  # Sắp xếp theo thứ tự mong muốn

# def get_iPhone_top_selling_phones():
#     top_phones_qs = (
#         PhoneVariant.objects
#         .filter(phone__brand='iPhone')
#         .values("phone")
#         .annotate(sold_quantity=Sum("sold_quantity"))
#         .order_by("-sold_quantity")
#     )

#     top_phone_ids = list(top_phones_qs.values_list("phone", flat=True)[:15])

#     min_variant = PhoneVariant.objects.filter(
#         phone=OuterRef("pk")
#     ).order_by("id").values("id")[:1]

#     sold_quantity_subquery = Subquery(
#         top_phones_qs.filter(phone=OuterRef("pk")).values("sold_quantity")
#     )

#     # Tạo danh sách When để giữ đúng thứ tự
#     order_case = Case(
#         *[When(id=phone_id, then=Value(index)) for index, phone_id in enumerate(top_phone_ids)],
#         output_field=IntegerField()
#     )

#     return Product.objects.filter(id__in=top_phone_ids).annotate(
#         variant_id=Subquery(min_variant),
#         img=Subquery(PhoneVariant.objects.filter(id=OuterRef("variant_id")).values("img")[:1]),
#         price=Subquery(PhoneVariant.objects.filter(id=OuterRef("variant_id")).values("price")[:1]),
#         sold_quantity=sold_quantity_subquery,
#         order_index=order_case  # Thêm trường này để sắp xếp
#     ).order_by("order_index")  # Sắp xếp theo thứ tự mong muốn

# def get_realme_top_selling_phones():
#     top_phones_qs = (
#         PhoneVariant.objects
#         .filter(phone__brand='Realme')
#         .values("phone")
#         .annotate(sold_quantity=Sum("sold_quantity"))
#         .order_by("-sold_quantity")
#     )

#     top_phone_ids = list(top_phones_qs.values_list("phone", flat=True)[:15])

#     min_variant = PhoneVariant.objects.filter(
#         phone=OuterRef("pk")
#     ).order_by("id").values("id")[:1]

#     sold_quantity_subquery = Subquery(
#         top_phones_qs.filter(phone=OuterRef("pk")).values("sold_quantity")
#     )

#     # Tạo danh sách When để giữ đúng thứ tự
#     order_case = Case(
#         *[When(id=phone_id, then=Value(index)) for index, phone_id in enumerate(top_phone_ids)],
#         output_field=IntegerField()
#     )

#     return Product.objects.filter(id__in=top_phone_ids).annotate(
#         variant_id=Subquery(min_variant),
#         img=Subquery(PhoneVariant.objects.filter(id=OuterRef("variant_id")).values("img")[:1]),
#         price=Subquery(PhoneVariant.objects.filter(id=OuterRef("variant_id")).values("price")[:1]),
#         sold_quantity=sold_quantity_subquery,
#         order_index=order_case  # Thêm trường này để sắp xếp
#     ).order_by("order_index")  # Sắp xếp theo thứ tự mong muốn
