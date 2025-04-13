from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import PhoneVariant, PhoneConfiguration
from django.contrib.auth import get_user_model
from apps.users.models import Client
from .models import Product, Rating
from django.utils import timezone


@api_view(["GET"])
def get_phone_variant(request):
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

@api_view(["POST"])
def create_rating(request):
    product_id = request.data.get("product_id")
    star = request.data.get("star")
    comment = request.data.get("comment", "")
    
    if not all([product_id, star]):
        return Response({"message": "Thiếu thông tin bắt buộc"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        star = int(star)
        if not 1 <= star <= 5:
            return Response({"message": "Số sao phải từ 1 đến 5"}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({"message": "Số sao không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Kiểm tra xem người dùng đã đăng nhập chưa
    if not request.user.is_authenticated:
        return Response({"message": "Bạn cần đăng nhập để đánh giá"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Lấy thông tin client từ user hiện tại
    try:
        
        client = Client.objects.get(username=request.user.username)
    except Client.DoesNotExist:
        return Response({"message": "Tài khoản không phải là khách hàng"}, status=status.HTTP_403_FORBIDDEN)
    
    # Lấy thông tin sản phẩm
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"message": "Sản phẩm không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
    
    # Kiểm tra xem đã đánh giá trước đó chưa
    rating, created = Rating.objects.get_or_create(
        product=product,
        client=client,
        defaults={"star": star, "comment": comment}
    )
    
    # Nếu đã tồn tại đánh giá, cập nhật lại
    if not created:
        rating.star = star
        rating.comment = comment
        rating.created_at = timezone.now()
        rating.save()
        message = "Cập nhật đánh giá thành công"
    else:
        message = "Thêm đánh giá thành công"
    
    return Response(
        {
            "message": message,
            "rating": {
                "id": rating.id,
                "product_id": rating.product.id,
                "client": rating.client.username.username,
                "star": rating.star,
                "comment": rating.comment,
                "created_at": rating.created_at
            }
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def get_product_ratings(request, product_id):
    """
    API trả về số lượng đánh giá theo từng mức sao của một sản phẩm
    """
    try:
        # Kiểm tra sản phẩm có tồn tại không
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"message": "Sản phẩm không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
    
    # Khởi tạo dictionary để lưu số lượng đánh giá theo từng mức sao
    ratings_count = {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0
    }
    
    # Đếm số lượng đánh giá cho từng mức sao
    for star in range(1, 6):
        count = Rating.objects.filter(product=product, star=star).count()
        ratings_count[str(star)] = count
    
    return Response(ratings_count, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_product_rating_details(request, product_id):
    """
    API trả về tất cả các đánh giá của một sản phẩm
    """
    try:
        # Kiểm tra sản phẩm có tồn tại không
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"message": "Sản phẩm không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
    
    # Lấy tất cả đánh giá của sản phẩm
    ratings = Rating.objects.filter(product=product).order_by('-created_at')
    
    # Chuyển đổi dữ liệu đánh giá thành định dạng JSON
    ratings_data = []
    for rating in ratings:  
        ratings_data.append({
            "id": rating.id,
            "client": rating.client.username.first_name + " " + rating.client.username.last_name,
            "star": rating.star,
            "comment": rating.comment,
            "created_at": rating.created_at
        })
    
    return Response({
        "product_id": product_id,
        "product_name": product.name,
        "ratings": ratings_data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_client_product_rating(request, product_id):
    """
    API trả về đánh giá của client hiện tại đối với một sản phẩm
    """
    # Kiểm tra xem người dùng đã đăng nhập chưa
    if not request.user.is_authenticated:
        return Response({"message": "Bạn cần đăng nhập để xem đánh giá của mình"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # Kiểm tra sản phẩm có tồn tại không
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"message": "Sản phẩm không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        # Tìm đánh giá của client hiện tại cho sản phẩm này
        client = Client.objects.get(username=request.user)
        rating = Rating.objects.get(product=product, client=client)
        
        # Trả về thông tin đánh giá
        return Response({
            "product_id": product_id,
            "client_id": client.id,
            "star": rating.star,
            "comment": rating.comment,
            "created_at": rating.created_at
        }, status=status.HTTP_200_OK)
        
    except Client.DoesNotExist:
        return Response({"message": "Không tìm thấy thông tin khách hàng"}, status=status.HTTP_404_NOT_FOUND)
    except Rating.DoesNotExist:
        # Trường hợp client chưa đánh giá sản phẩm này
        return Response({
            "product_id": product_id,
            "message": "Bạn chưa đánh giá sản phẩm này",
            "star": 0
        }, status=status.HTTP_200_OK)

