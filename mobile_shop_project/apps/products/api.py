from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import PhoneVariant, PhoneConfiguration, Phone, Category
from django.contrib.auth import get_user_model
from apps.users.models import Client,CustomUser 
from .models import Product, Rating
from django.utils import timezone
from django.db import models


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

@api_view(['POST'])
def search_products_by_name(request):
    """
    API tìm kiếm sản phẩm theo tên và trả về thông tin cơ bản kèm hình ảnh đại diện
    """
    search_query = request.data.get('search_query', '')
    
    if not search_query:
        return Response({"message": "Vui lòng nhập từ khóa tìm kiếm"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Tìm các phone có tên chứa search_query (không phân biệt hoa thường)
        phones = Phone.objects.filter(name__icontains=search_query)
        
        results = []
        for phone in phones:
            # Lấy phone_variant đầu tiên của mỗi phone để lấy hình ảnh đại diện
            first_variant = PhoneVariant.objects.filter(phone=phone).first()
            
            if first_variant:
                results.append({
                    'id': phone.id,
                    'name': phone.name,
                    'brand': phone.brand,
                    'image_url': first_variant.img.url if first_variant.img else None,
                    'min_price': first_variant.price  # Giá của variant đầu tiên
                })
        
        return Response({
            'count': len(results),
            'results': results
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"message": f"Lỗi khi tìm kiếm: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def add_new_phone(request):
    """
    API thêm điện thoại mới vào hệ thống
    """
    # Kiểm tra xem người dùng đã đăng nhập chưa
    if not request.user.is_authenticated:
        return Response({
            "message": "Bạn cần đăng nhập để thực hiện chức năng này"
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Kiểm tra xem người dùng có phải là nhân viên không
    try:
        user = CustomUser.objects.get(username=request.user.username)
        if user.role != 'staff' and user.role != 'admin':
            return Response({
                "message": "Bạn không có quyền thực hiện chức năng này"
            }, status=status.HTTP_403_FORBIDDEN)
    except CustomUser.DoesNotExist:
        return Response({
            "message": "Không tìm thấy thông tin người dùng"
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Lấy dữ liệu từ request
        name = request.data.get('name')
        brand = request.data.get('brand')
        phone_status = request.data.get('status', 'Đang kinh doanh')
        youtube_link = request.data.get('youtube_link', '')
        
        # Thông số kỹ thuật
        screen = request.data.get('screen', '')
        cpu = request.data.get('cpu', '')
        rom = request.data.get('rom', '')
        ram = request.data.get('ram', '')
        front_camera = request.data.get('front_camera', '')
        back_camera = request.data.get('back_camera', '')
        battery = request.data.get('battery', '')
        charger = request.data.get('charger', '')
        speaker = request.data.get('speaker', '')
        
        # Kiểm tra dữ liệu bắt buộc
        if not name or not brand:
            return Response({
                "message": "Thiếu thông tin bắt buộc (tên, thương hiệu)"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Kiểm tra xem tên điện thoại đã tồn tại chưa
        if Phone.objects.filter(name=name).exists():
            return Response({
                "message": f"Điện thoại có tên '{name}' đã tồn tại trong hệ thống"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Tự động lấy hoặc tạo danh mục "Điện thoại"
        category, created = Category.objects.get_or_create(name="Điện thoại")
        
        # Tạo điện thoại mới
        phone = Phone.objects.create(
            name=name,
            brand=brand,
            status=phone_status,
            category=category,
            youtube_link=youtube_link,
            screen=screen,
            cpu=cpu,
            rom=rom,
            ram=ram,
            front_camera=front_camera,
            back_camera=back_camera,
            battery=battery,
            charger=charger,
            speaker=speaker
        )
        
        return Response({
            "message": "Thêm điện thoại mới thành công",
            "phone_id": phone.id,
            "phone_name": phone.name
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            "message": f"Lỗi khi thêm điện thoại mới: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def add_phone_variant(request):
    """
    API thêm biến thể điện thoại mới
    """
    # Kiểm tra xem người dùng đã đăng nhập chưa
    if not request.user.is_authenticated:
        return Response({
            "message": "Bạn cần đăng nhập để thực hiện chức năng này"
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Kiểm tra xem người dùng có phải là nhân viên không
    try:
        user = CustomUser.objects.get(username=request.user.username)
        if user.role != 'staff' and user.role != 'admin':
            return Response({
                "message": "Bạn không có quyền thực hiện chức năng này"
            }, status=status.HTTP_403_FORBIDDEN)
    except CustomUser.DoesNotExist:
        return Response({
            "message": "Không tìm thấy thông tin người dùng"
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Lấy dữ liệu từ request
        phone_id = request.data.get('phone_id')
        ram = request.data.get('ram')
        rom = request.data.get('rom')
        color = request.data.get('color')
        price = request.data.get('price')
        stock = request.data.get('stock', 0)
        img = request.FILES.get('img')
        
        # Kiểm tra dữ liệu bắt buộc
        if not all([phone_id, ram, rom, color, price, stock, img]):
            return Response({
                "message": "Thiếu thông tin bắt buộc (phone_id, ram, rom, color, price, stock, img)"
            }, status=status.HTTP_400_BAD_REQUEST)
        # Kiểm tra phone_id có tồn tại không
        try:
            phone = Phone.objects.get(id=phone_id)
        except Phone.DoesNotExist:
            return Response({
                "message": f"Không tìm thấy điện thoại với ID {phone_id}"
            }, status=status.HTTP_404_NOT_FOUND)
            
            # Lấy hoặc tạo cấu hình
        configuration, created = PhoneConfiguration.objects.get_or_create(
            ram=ram,
            rom=rom
        )
        
        # Kiểm tra xem biến thể này đã tồn tại chưa
        if PhoneVariant.objects.filter(phone=phone, configuration=configuration, color=color).exists():
            return Response({
                "message": f"Biến thể với RAM {ram}, ROM {rom}, màu {color} của điện thoại này đã tồn tại"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Kiểm tra price
        try:
            price = float(price)
            if price <= 0:
                return Response({
                    "message": "Giá phải lớn hơn 0"
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({
                "message": "Giá không hợp lệ"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Kiểm tra stock
        try:
            stock = int(stock)
            if stock < 0:
                return Response({
                    "message": "Số lượng tồn kho không được âm"
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({
                "message": "Số lượng tồn kho không hợp lệ"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Tạo biến thể mới
        phone_variant = PhoneVariant.objects.create(
            phone=phone,
            configuration=configuration,
            color=color,
            price=price,
            stock=stock,
            sold_quantity=0
        )
        
        # Cập nhật hình ảnh nếu có
        if img:
            phone_variant.img = img
            phone_variant.save()
        
        return Response({
            "message": "Thêm biến thể điện thoại thành công",
            "variant_id": phone_variant.id,
            "phone_name": phone.name,
            "configuration": f"{ram}/{rom}",
            "color": color,
            "price": price,
            "stock": stock
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            "message": f"Lỗi khi thêm biến thể điện thoại: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



