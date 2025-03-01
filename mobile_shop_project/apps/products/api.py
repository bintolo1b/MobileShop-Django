from django.http import JsonResponse
from .models import PhoneVariant, PhoneConfiguration
from django.shortcuts import get_object_or_404

def get_phone_variant(request):
    phone_id = request.GET.get('phone_id')
    ram = request.GET.get('ram')
    rom = request.GET.get('rom')
    color = request.GET.get('color')

    print(f"phone_id: {phone_id}, ram: {ram}, rom: {rom}, color: {color}")
    configuration = get_object_or_404(PhoneConfiguration, ram = ram, rom = rom)
    phone_variant = get_object_or_404(PhoneVariant, phone_id = phone_id, configuration = configuration, color = color)

    return JsonResponse({
        "id": phone_variant.id,
        "phone_id": phone_variant.phone.id,
        "ram": phone_variant.configuration.ram,
        "rom": phone_variant.configuration.rom,
        "color": phone_variant.color,
        "price": phone_variant.price,
        "stock": phone_variant.stock,
        "sold_quantity": phone_variant.sold_quantity,
        "image": phone_variant.img.url if phone_variant.img else None
    })