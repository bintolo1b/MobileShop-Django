from apps.products.models import PhoneVariant, Phone, Product

def get_name_of_phone_variant(phone_variant_id):
    try:
        # Lấy phone_variant
        phone_variant = PhoneVariant.objects.get(id=phone_variant_id)
        
        # Từ phone_variant -> phone -> product -> name
        phone_name = phone_variant.phone.name
        
        return phone_name
    except PhoneVariant.DoesNotExist:
        return None

    
