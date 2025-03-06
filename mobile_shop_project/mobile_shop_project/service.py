from apps.products.models import Phone, PhoneVariant, Product
from django.db.models import Case, When, IntegerField, Sum, Value, Subquery, OuterRef, QuerySet

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

    return Product.objects.filter(id__in=top_phone_ids).annotate(
        variant_id=Subquery(min_variant),
        img=Subquery(PhoneVariant.objects.filter(id=OuterRef("variant_id")).values("img")[:1]),
        price=Subquery(PhoneVariant.objects.filter(id=OuterRef("variant_id")).values("price")[:1]),
        sold_quantity=sold_quantity_subquery,
        order_index=order_case  # Thêm trường này để sắp xếp
    ).order_by("order_index")  # Sắp xếp theo thứ tự mong muốn

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
