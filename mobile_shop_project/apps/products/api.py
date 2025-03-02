from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import PhoneVariant, PhoneConfiguration
from django.contrib.auth import get_user_model

@api_view(["GET"])
def get_phone_variant(request):
    print(get_user_model())
    phone_id = request.query_params.get("phone_id")
    ram = request.query_params.get("ram")
    rom = request.query_params.get("rom")
    color = request.query_params.get("color")

    print(f"phone_id: {phone_id}, ram: {ram}, rom: {rom}, color: {color}")

    if not all([phone_id, ram, rom, color]):
        return Response({"message": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

    configuration = get_object_or_404(PhoneConfiguration, ram=ram, rom=rom)
    phone_variant = get_object_or_404(PhoneVariant, phone_id=phone_id, configuration=configuration, color=color)

    return Response(
        {
            "id": phone_variant.id,
            "phone_id": phone_variant.phone.id,
            "ram": phone_variant.configuration.ram,
            "rom": phone_variant.configuration.rom,
            "color": phone_variant.color,
            "price": phone_variant.price,
            "stock": phone_variant.stock,
            "sold_quantity": phone_variant.sold_quantity,
            "image": phone_variant.img.url if phone_variant.img else None,
        },
        status=status.HTTP_200_OK,
    )
